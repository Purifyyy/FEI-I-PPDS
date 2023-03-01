"""
Sleeping Barber Problem simulation.

This script simulates the Sleeping Barber Problem, where customers arrive at a barber shop and
either get a haircut or leave if there are no empty seats in the waiting room. There is only
one barber in the shop who can cut hair.
"""


__authors__ = "Tomáš Baďura, Marián Šebeňa, Tomáš Vavro"


from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint


class Shared(object):
    """
    This class represents the shared state of the barber shop simulation.

    Attributes:
        mutex (Mutex) -- a mutex lock to provide mutual exclusion between customers
        waiting_room (int) -- the number of available seats in the waiting room
        customer (Semaphore) -- a semaphore to signal the barber when a customer arrives
        barber (Semaphore) -- a semaphore to signal the customer when the barber is ready to cut hair
        customer_done (Semaphore) -- a semaphore to signal the barber when the customer's haircut is done
        barber_done (Semaphore) -- a semaphore to signal the customer when the barber finishes cutting
    """
    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """
    Simulates a customer getting his hair cut.

    Arguments:
        i (int) -- the ID of the customer
    """
    print(f"Customer {i} is getting a haircut")
    sleep(randint(36, 50) / 100)


def cut_hair():
    """
    Simulates a barber cutting customer's hair.
    """
    print("Barber is cutting hair")
    sleep(randint(30, 35) / 100)

def balk(i):
    """
    Simulates a customer leaving for some time, upon arriving at a full waiting room.

    Arguments:
        i (int) -- the ID of the customer
    """
    print(f"\033[91mCustomer {i} entered a full waiting room\033[00m *sigh*")
    sleep(randint(20, 30) / 100)


def growing_hair(i):
    """
    Simulates a growth of customer's hair.

    Arguments:
        i (int) -- the ID of the customer
    """
    sleep(randint(100, 200) / 100)


def customer(i, shared):
    """
    Simulates a customer visiting the barber shop.

    A customer who enters the barber shop, checks for the availability of the barber,
    sits in the waiting room if the barber is busy, and leaves the barber shop if
    there is no available seat in the waiting room.

    Arguments:
        i (int) -- the ID of the customer
        shared (Shared) -- an instance of the Shared class containing semaphores and other shared variables
    """
    while True:
        shared.mutex.lock()

        if shared.waiting_room < N:    # check if there is space in waiting room
            print(f"\033[92mCustomer {i} SAT DOWN in the waiting room chair\033[00m")
            shared.waiting_room += 1
            shared.mutex.unlock()

            shared.customer.signal()    # wake up barber
            shared.barber.wait()    # wait for the barber to get ready to cut hair

            get_haircut(i)

            shared.barber_done.wait()   # wait for barber to finish cutting hair
            shared.customer_done.signal()   # customer is done getting a haircut

            shared.mutex.lock()
            shared.waiting_room -= 1
            print(f"\033[93mCustomer {i} LEFT the barber shop\033[00m")
            shared.mutex.unlock()
            growing_hair(i)
            continue

        shared.mutex.unlock()   # no seats in waiting room available, balk out
        balk(i)


def barber(shared):
    """
    Simulates a barber who cuts hair for customers.

    Barber sleeps while waiting for a customer to arrive in the waiting room. Upon customers arrival,
    the barber is notified and proceeds to signal that he is ready to cut hair.

    Arguments:
        shared (Shared) -- an instance of the Shared class containing semaphores and other shared variables
    """
    while True:
        shared.customer.wait()  # sleep until a customer arrives
        shared.barber.signal()  # indicate readiness to cut hair

        cut_hair()

        shared.barber_done.signal()  # barber is done cutting the hair
        shared.customer_done.wait()  # wait for customer to be finished getting a haircut


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()

C = 5 # number of customers
N = 3 # size of waiting room

if __name__ == "__main__":
    main()
"""
Program represents different sequences of using mutex

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__authors__ = "Tomáš Baďura, Marián Šebeňa, Tomáš Vavro"


from fei.ppds import Mutex, Thread, Semaphore
from time import sleep
from random import randint


class Shared(object):

    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    print(f"Customer {i} is getting a haircut")
    sleep(0.5)


def cut_hair():
    print("Barber is cutting hair")
    sleep(0.5)

def balk(i):
    print(f"Customer {i} entered a full waiting room *sigh*")
    sleep(0.25)


def growing_hair(i):
    sleep(1)



def customer(i, shared):
    while True:
        shared.mutex.lock()

        if shared.waiting_room < N:
            print(f"Customer {i} sat down in the waiting room chair")
            shared.waiting_room += 1
            shared.mutex.unlock()

            shared.customer.signal()
            shared.barber.wait()

            get_haircut(i)

            shared.customer_done.signal()
            shared.barber_done.wait()

            shared.mutex.lock()
            shared.waiting_room -= 1
            shared.mutex.unlock()
            growing_hair(i)
            continue

        shared.mutex.unlock()
        balk(i)


def barber(shared):
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


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
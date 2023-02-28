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
    sleep(0.1)


def cut_hair():
    sleep(0.1)


def balk(i):
    sleep(0.25)



def growing_hair(i):
    sleep(1)



def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        shared.mutex.lock()

        if shared.waiting_room < N:
            shared.waiting_room += 1
            shared.mutex.unlock()

            # TODO: Rendezvous 1
            get_haircut(i)
            # TODO: Rendezvous 2

            shared.mutex.lock()
            shared.waiting_room -= 1
            shared.mutex.unlock()
            growing_hair(i)
            continue

        shared.mutex.unlock()
        balk(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


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
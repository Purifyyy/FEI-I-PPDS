"""
Sophisticated savages feast simulation.

A simulation where a group of "savages" share a communal pot of food.
Each savage takes one serving from the pot, and when it's empty,
cooks refill it. The cooks can only refill the pot one portion by one
when all the savages are not currently eating.
"""


__authors__ = "Tomáš Baďura, Marián Šebeňa"


from fei.ppds import Thread, Mutex, Semaphore, print, Event
from time import sleep

H: int = 5  # number of portions in a full pot
D: int = 3  # number of savages
K: int = 4  # number of cooks


class Shared:
    """
    This class that represents the shared resources among the savages and cooks.

    Attributes:
        pot (int) -- the number of portions remaining in the pot of food
        savage_mutex (Mutex) -- a mutex lock to provide mutual exclusion between savages
        cook_mutex (Mutex) -- a mutex lock providing mutual exclusion between cooks
        full_pot (Semaphore) -- a semaphore to signal the savages that the pot has been refilled
        empty_pot (Event) -- an event that the cooks wait for, and the savages signal, when in need of pot refill
        barrier_count (int) -- savages count, when going through the tourniquet
        barrier_mutex (Mutex) -- a lock that ensures mutual exclusion when going through tourniquet
        turnstile1 (Semaphore) -- a semaphore that serves as an entrance tourniquet
        turnstile2 (Semaphore) -- semaphore serving as an exit tourniquet
    """
    def __init__(self):
        self.pot = H
        self.savage_mutex = Mutex()
        self.cook_mutex = Mutex()
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.barrier_count = 0
        self.barrier_mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)


def put_portion(i: int, shared: Shared):
    """
    Simulates a cook adding a cooked portion to a shared food pot.

    Arguments:
        i (int) -- the identifier of the cook
        shared (Shared) -- an instance of the Shared class containing shared resources and variables
    """
    shared.pot += 1
    print(f"\033[34mCook [{i}]: I've added a portion. [{shared.pot}/{H}]\033[00m")


def get_portion(i: int, shared: Shared):
    """
    Simulates a savage taking a portion out of the shared food pot.

    Arguments:
        i (int) -- the identifier of the savage
        shared (Shared) -- an instance of the Shared class containing shared resources and variables
    """
    shared.pot -= 1
    print(f"Savage [{i}]: I've took a portion and I'm going to eat now. [{shared.pot}/{H} left]")


def cook(i: int, shared: Shared):
    """
    Simulates a cook preparing and adding a food portion to the food pot.

    Cook prepares a food portion and waits until the pot gets empty,
    then checks whether the pot if fully refilled, if not he adds his
    portion, if yes he signals other cooks, and they wait again.

    Arguments:
        i (int) -- the identifier of the cook
        shared (Shared) -- an instance of the Shared class containing shared resources and variables
    """
    while True:

        sleep(0.3)  # cooking a portion

        shared.cook_mutex.lock()
        shared.empty_pot.wait()  # wait for the savages to empty the pot
        if shared.pot == H:
            shared.empty_pot.clear()  # reset event to waiting state for the cooks
            shared.full_pot.signal()  # signal savages to continue feasting
            shared.cook_mutex.unlock()
            print(f"\033[92mCook [{i}]: The pot is full, savages may continue.\033[00m")
            continue
        put_portion(i, shared)
        shared.cook_mutex.unlock()


def savage(i: int, shared: Shared):
    """
    Simulates a savage participating in the feast.

    Savage waits until all savages are present, once that occurs
    he takes a portion of the food from the pot and starts eating.
    If there is no food left in the pot, he signals the cooks to
    refill it. Once all the savages finish eating, this process
    repeats.

    Arguments:
        i (int) -- the identifier of the cook
        shared (Shared) -- an instance of the Shared class containing shared resources and variables
    """
    while True:

        shared.barrier_mutex.lock()
        shared.barrier_count += 1
        if shared.barrier_count == D:
            shared.turnstile1.signal(D)
            print(f"\033[36mWe're all here, let the feast begin.\033[00m")
        shared.barrier_mutex.unlock()
        shared.turnstile1.wait()

        shared.savage_mutex.lock()
        if shared.pot == 0:
            print(f"\033[31mSavage [{i}]: There is no food left, I'm waking up the cooks.\033[00m")
            shared.empty_pot.signal()
            shared.full_pot.wait()  # wait for the cooks to refill the pot
        get_portion(i, shared)
        shared.savage_mutex.unlock()

        sleep(0.2)  # eating a portion

        shared.barrier_mutex.lock()
        shared.barrier_count -= 1
        if shared.barrier_count == 0:
            shared.turnstile2.signal(D)
        shared.barrier_mutex.unlock()
        shared.turnstile2.wait()


def main():
    shared: Shared = Shared()
    threads = list()

    for i in range(D):
        threads.append(Thread(savage, i, shared))
    for i in range(K):
        threads.append(Thread(cook, i, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()

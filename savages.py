"""

Dinning savages simulation.

"""


__authors__ = "Tomáš Baďura"


from fei.ppds import Thread, Mutex, Semaphore, print, Event
from time import sleep

H: int = 10  # number of portions in a full pot
D: int = 3  # number of savages
K: int = 4  # number of cooks


class Shared:
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
    shared.pot += 1
    print(f"Cook {i}: [{shared.pot}/{H}]")


def get_portion(i: int, shared: Shared):
    print(f"Savage [{i}]: I'm taking a portion")
    shared.pot -= 1


def cook(i: int, shared: Shared):
    while True:
        shared.empty_pot.wait()
        shared.cook_mutex.lock()
        shared.empty_pot.wait()
        put_portion(i, shared)
        if shared.pot == H:
            shared.empty_pot.clear()
            shared.full_pot.signal()
            shared.cook_mutex.unlock()
        shared.cook_mutex.unlock()


def savage(i: int, shared: Shared):
    while True:

        shared.barrier_mutex.lock()
        shared.barrier_count += 1
        if shared.barrier_count == D:
            shared.turnstile1.signal(D)
        shared.barrier_mutex.unlock()
        shared.turnstile1.wait()

        shared.savage_mutex.lock()
        if shared.pot == 0:
            print(f"Savage [{i}]: There is no food left, I'm waking up the chefs")
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_portion(i, shared)
        shared.savage_mutex.unlock()

        sleep(0.2)  # pseudo-eating state

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

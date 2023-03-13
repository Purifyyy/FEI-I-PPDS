"""

Dinning savages simulation.

"""


__authors__ = "Tomáš Baďura"


from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

H: int = 5  # number of portions in a full pot
D: int = 3  # number of savages
K: int = 2  # number of cooks


class Shared:
    def __init__(self):
        self.pot = H
        self.mutex = Mutex()
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(K)

        self.barrier_count = 0
        self.barrier_mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)


def put_portion(i: int, shared: Shared):
    print(f"put_portion {i}")


def get_portion(i: int, shared: Shared):
    print(f"Savage [{i}]: I'm taking a portion")
    shared.pot -= 1


def cook(i: int, shared: Shared):
    print(f"cook {i}")


def savage(i: int, shared: Shared):
    while True:

        shared.barrier_mutex.lock()
        shared.barrier_count += 1
        if shared.barrier_count == D:
            shared.turnstile1.signal(D)
        shared.barrier_mutex.unlock()
        shared.turnstile1.wait()

        # everyone ready, set, feast

        shared.barrier_mutex.lock()
        shared.barrier_count -= 1
        if shared.barrier_count == 0:
            shared.turnstile2.signal(D)
        shared.barrier_mutex.unlock()
        shared.turnstile2.wait()

        shared.mutex.lock()
        if shared.pot == 0:
            print(f"Savage [{i}]: There is no food left, I'm waking up the chefs")
            shared.empty_pot.signal(K)
            shared.full_pot.wait()
        get_portion(i, shared)
        shared.mutex.unlock()

        sleep(0.2)  # pseudo-eating state


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

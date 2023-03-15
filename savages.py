"""

Dinning savages simulation.

"""


__authors__ = "Tomáš Baďura, Marián Šebeňa"


from fei.ppds import Thread, Mutex, Semaphore, print, Event
from time import sleep

H: int = 5  # number of portions in a full pot
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
    print(f"\033[34mCook [{i}]: I've added a portion. [{shared.pot}/{H}]\033[00m")


def get_portion(i: int, shared: Shared):
    shared.pot -= 1
    print(f"Savage [{i}]: I've took a portion. [{shared.pot}/{H} left]")


def cook(i: int, shared: Shared):
    while True:

        sleep(0.3)  # cooking a portion

        shared.cook_mutex.lock()
        shared.empty_pot.wait()
        if shared.pot == H:
            shared.empty_pot.clear()
            shared.full_pot.signal()
            shared.cook_mutex.unlock()
            print(f"\033[92mCook [{i}]: The pot is full, savages may continue.\033[00m")
            continue
        put_portion(i, shared)
        shared.cook_mutex.unlock()


def savage(i: int, shared: Shared):
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
            shared.full_pot.wait()
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

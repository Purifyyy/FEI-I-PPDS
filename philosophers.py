"""
Dinning philosophers problem simulation.

"""


__authors__ = "Tomáš Baďura, Tomáš Vavro"


from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    def __init__(self):
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def philosopher(i: int, shared: Shared):
    for _ in range(NUM_RUNS):
        think(i)

        sleep(0.5)
        if i == 0:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            shared.forks[i].lock()
        else:
            shared.forks[i].lock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
        eat(i)
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()


def main():
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()

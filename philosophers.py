"""
Dinning philosophers problem simulation.

This module defines a solution to the Dining Philosophers problem,
which involves five philosophers sitting around a table, alternating
between thinking and eating, and using forks.
"""


__authors__ = "Tomáš Baďura, Tomáš Vavro"


from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """
    This class that represents the shared resources among the philosophers, i.e., the forks.

    Attributes:
        forks (list) -- a list of Mutex objects, one for each fork on the table
    """
    def __init__(self):
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """
    Simulates a philosopher thinking.

    Arguments:
        i (int) -- the identifier of the philosopher
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    """
    Simulates a philosopher eating a meal.

    Arguments:
        i (int) -- the identifier of the philosopher
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def philosopher(i: int, shared: Shared):
    """
    Simulates a process of thinking, eating of a philosopher.

    A philosopher thinks, when he gets hungry, he attempts to raise forks on both of his sides.
    If both forks are not available, the philosopher will wait until they become available.
    Once the philosopher has finished eating, they will put down both of the forks and return
    to a state of thinking.

    Arguments:
        i (int) -- the identifier of the philosopher
        shared (Shared) -- an instance of the Shared class containing a list of fork mutexes
    """
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

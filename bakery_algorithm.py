"""This module contains an implementation of bakery algorithm.

The Bakery Algorithm is a mutual exclusion algorithm, which is used to ensure,
that only one thread can enter a critical section of code at any given time.
"""

__authors__ = "Tomáš Vavro, Tomáš Baďura"

from fei.ppds import Thread
from time import sleep

NUM_THREADS: int = 8
num: list[int] = [0] * NUM_THREADS
num_in: list[int] = [0] * NUM_THREADS


def bakery_alg(tid: int):
    """Grant exclusive access to critical section, to thread with id tid

    Once it's the threads' turn, it can enter the critical section and perform its task,
    using shared resources. While performing the task, it is insured that no other thread
    may enter the critical section.

    Arguments:
        tid -- thread id
    """
    global num, num_in, NUM_THREADS
    # thread's state is changed to '1', indicating that it's currently in the process of acquiring a ticket number
    num_in[tid] = 1
    # thread is assigned a unique ticket number, that's greater than any ticket number currently held by other threads
    num[tid] = max(num) + 1
    num_in[tid] = 0

    for j in range(NUM_THREADS):
        while num_in[j]:
            pass
        # thread with lower ticket number is allowed to entry the critical section
        # if threads hold the same ticket number, thread id is used as a tiebreaker
        while num[j] != 0 and (num[j] < num[tid] or (num[j] == num[tid] and j < tid)):
            pass

    # beginning of critical section
    print(f"Process {tid} runs a complicated computation!")
    sleep(1)
    # end of critical section
    num[tid] = 0


if __name__  == '__main__':
    threads = [Thread(bakery_alg, i) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
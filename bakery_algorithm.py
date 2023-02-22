from fei.ppds import Thread
from time import sleep

NUM_THREADS: int = 8
num: list[int] = [0] * NUM_THREADS
num_in: list[int] = [0] * NUM_THREADS


def bakery_alg(tid: int):
    global num, num_in, NUM_THREADS
    num_in[tid] = 1
    num[tid] = max(num) + 1
    num_in[tid] = 0

    for j in range(NUM_THREADS):
        while num_in[j]:
            pass
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
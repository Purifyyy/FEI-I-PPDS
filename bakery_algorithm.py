from fei.ppds import Thread
from time import sleep

num_threads: int = 8
num: list[int] = [0] * num_threads
num_in: list[int] = [0] * num_threads


def bakery_alg(tid: int):
    global num, num_in, num_threads
    i = tid
    num_in[i] = 1
    num[i] = max(num) + 1
    num_in[i] = 0

    for j in range(num_threads):
        while num_in[j]:
            pass
        while num[j] != 0 and (num[j] < num[i] or (num[j] == num[i] and j < i)):
            pass

    # beginning of critical section
    print(f"Process {i} runs a complicated computation!")
    sleep(1)
    # end of critical section

    num[i] = 0


if __name__ == '__main__':
    threads = [Thread(bakery_alg, i) for i in range(num_threads)]
    [t.join() for t in threads]

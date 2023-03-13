"""

Dinning savages simulation.

"""


__authors__ = "Tomáš Baďura"


from fei.ppds import Thread, Mutex, print
from time import sleep

H: int = 5  # number of portions in a full pot
D: int = 3  # number of savages
K: int = 2  # number of cooks


class Shared:
    def __init__(self):
        self.pot = H


def put_portion(i: int, shared: Shared):
    print(f"put_portion {i}")


def get_portion(i: int, shared: Shared):
    print(f"get_portion {i}")


def cook(i: int, shared: Shared):
    print(f"cook {i}")


def savage(i: int, shared: Shared):
    print(f"savage {i}")


def main():
    shared: Shared = Shared()
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(D)
    ]
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i in range(K)
    ]
    for s in savages:
        s.join()
    for c in cooks:
        c.join()


if __name__ == "__main__":
    main()

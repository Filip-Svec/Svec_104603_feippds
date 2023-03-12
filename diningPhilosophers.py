"""This module implements dinning philosophers problem.

Implementation uses left and right-handed philosophers
to solve this problem.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Filip Švec, Tomáš Vavro"
__email__ = "xsvecf@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_PHILOSOPHERS = 6
NUM_RUNS = 10


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i):
    """Simulate thinking.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i):
    """Simulate eating.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def philosopher(i, shared):
    """Run philosopher's code.

    Args:
        i -- philosopher's id
        shared -- shared data
    """

    # choosing which fork to pick up first (left or right)
    is_right_handed = i % 2 == 0
    if is_right_handed:
        first_fork = (i + 1) % NUM_PHILOSOPHERS
        second_fork = i
    else:
        first_fork = i
        second_fork = (i + 1) % NUM_PHILOSOPHERS

    for _ in range(NUM_RUNS):
        think(i)

        # simulate picking up the forks
        shared.forks[first_fork].lock()
        shared.forks[second_fork].lock()

        # only eating after acquiring both forks
        eat(i)

        # simulate putting down the forks
        shared.forks[first_fork].unlock()
        shared.forks[second_fork].unlock()


def main():
    """Run main."""
    shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()

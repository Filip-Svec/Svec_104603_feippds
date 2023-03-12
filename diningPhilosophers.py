"""This module implements left and right-handed dinning philosophers problem.


"""

__author__ = "Filip Švec, Tomáš Vavro"
__email__ = "xsvecf@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_PHILOSOPHERS = 10
NUM_RUNS = 10


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def philosopher():
    """Run philosopher's code.

    Args:
        i -- philosopher's id
        shared -- shared data
    """


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

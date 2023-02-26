"""This module contains an implementation of bakery algorithm.


"""

__author__ = "Filip Švec, Tomáš Vavro"
__email__ = "xsvecf@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

# number of threads
NUM_THREADS = 5
choosing = [False] * NUM_THREADS
ticket_number = [0] * NUM_THREADS


def lock(tid):
    """Simulates a locking process.
    Arguments:
        tid      -- thread id
    """

    # process chooses its ticket number
    choosing[tid] = True
    ticket_number[tid] = max(ticket_number) + 1
    choosing[tid] = False

    for j in range(NUM_THREADS):
        # first loop waits for threads to choose their number
        while choosing[j]:
            sleep(0.001)

        # second loop checks whether the current thread has the lowest number
        while ticket_number[j] != 0 and (ticket_number[j], j) < (ticket_number[tid], tid):
            sleep(0.001)


def unlock(tid):
    """Sets ticket number to 0 when thread leaves the critical section.
    Arguments:
        tid      -- thread id
    """
    ticket_number[tid] = 0


def critical_section(tid):
    """Simulates a process in critical section.
    Arguments:
        tid      -- thread id
    """
    print(f'Thread {tid} enters critical section')
    sleep(1)
    print(f'Thread {tid} exits critical section')


def process(tid):
    """Encapsulates the whole process and runs it N number of times.
    Arguments:
        tid      -- thread id
    """
    num_of_runs = 4
    for i in range(num_of_runs):
        lock(tid)
        critical_section(tid)
        unlock(tid)


if __name__ == '__main__':
    # creating threads and running the process within them
    threads = [Thread(process, i) for i in range(NUM_THREADS)]

    # waits for every thread to finish before main program finishes
    for thread in threads:
        thread.join()

"""This module contains the implementation of bakery algorithm


"""

__author__ = "Filip Švec, Tomáš Vavro"
__email__ = "xsvecf@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

NUM_THREADS = 5
choosing = [False] * NUM_THREADS
ticket_number = [0] * NUM_THREADS


def lock(tid):
    choosing[tid] = True
    ticket_number[tid] = max(ticket_number) + 1
    choosing[tid] = False

    for j in range(NUM_THREADS):
        while choosing[j]:
            sleep(0.001)
        while ticket_number[j] != 0 and (ticket_number[j], j) < (ticket_number[tid], tid):
            sleep(0.001)


def unlock(tid):
    ticket_number[tid] = 0


def critical_section(tid):
    print(f'Thread {tid} enters critical section')
    sleep(1)
    print(f'Thread {tid} exits critical section')


def process(tid):
    num_of_runs = 4
    for i in range(num_of_runs):
        lock(tid)
        critical_section(tid)
        unlock(tid)


if __name__ == '__main__':
    threads = [Thread(process, i) for i in range(NUM_THREADS)]
    for thread in threads:
        thread.join()

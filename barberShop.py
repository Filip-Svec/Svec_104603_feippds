"""This module contains an implementation of sleeping barber.

This algorithm implements semaphores in order to allow or deny access
to shared the resources.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Filip Švec, Marián Šebeňa"
__email__ = "xsvecf@stuba.sk, mariansebena@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, print, Semaphore
from time import sleep
from random import randint


class Shared(object):
    """"Object Shared for multiple threads using demonstration"""
    def __init__(self):
        """"Shared class constructor"""

        # Initialized semaphores and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    print(f"CUSTOMER {i} is getting a haircut.")
    sleep(randint(1, 3))


def cut_hair():
    print("BARBER is cutting hair.")
    sleep(randint(1, 3))


def balk(i):
    print(f"Waiting room is FULL, CUSTOMER {i} is leaving.")
    sleep(randint(1, 3))


def growing_hair(i):
    print(f"CUSTOMER {i} is growing hair.")
    sleep(randint(1, 3))


def customer(i, shared):
    while True:
        shared.mutex.lock()
        if shared.waiting_room < N:
            shared.waiting_room += 1
            print(f"Customer {i} has entered the waiting room, SEATS occupied: {shared.waiting_room}")
            shared.customer.signal()
            shared.mutex.unlock()
            shared.barber.wait()
            get_haircut(i)
            shared.customer_done.signal()
            print(f"Customer {i} is done and leaving")
            growing_hair(i)
            shared.barber_done.wait()

        else:
            shared.mutex.unlock()
            balk(i)


def barber(shared):
    while True:
        shared.customer.wait()
        shared.mutex.lock()
        shared.waiting_room -= 1
        shared.mutex.unlock()
        shared.barber.signal()
        cut_hair()
        shared.customer_done.wait()
        print(f"Barber is DONE cutting hair")
        shared.barber_done.signal()


def main():
    shared = Shared()
    customers = []

    # creating threads and running the process within them
    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    # waits for every thread to finish before main program finishes
    for t in customers + [hair_stylist]:
        t.join()


# C = numOfCustomers N = 3 sizeOfWaitingRoom
C = 5
N = 3

if __name__ == "__main__":
    main()

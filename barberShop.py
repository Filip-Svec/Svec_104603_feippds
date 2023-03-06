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
        self.customer = Semaphore(0)  # Semaphore to signal the barber that a customer is ready to get a haircut
        self.barber = Semaphore(0)  # Semaphore to signal the customer that the barber is ready to cut hair
        self.customer_done = Semaphore(0)  # Semaphore to signal the barber that the customer is done getting a haircut
        self.barber_done = Semaphore(0)  # Semaphore to signal the customer that the barber is done cutting hair


def get_haircut(i):
    print(f"CUSTOMER {i} is getting a haircut.")
    sleep(randint(1, 3))


def cut_hair():
    print("\nBARBER is cutting hair.\n")
    sleep(randint(1, 3))


def balk(i):
    print(f"Waiting room is FULL, CUSTOMER {i} is leaving.")
    sleep(randint(1, 3))


def growing_hair(i):
    print(f"CUSTOMER {i} is growing hair.")
    sleep(randint(1, 3))


def customer(i, shared):
    """Simulates customers behavior
    Arguments:
        i      -- thread id (customer)
        shared -- object of class Shared
    """
    while True:

        # lock thread and enter the room if seat is available
        shared.mutex.lock()
        if shared.waiting_room < N:
            shared.waiting_room += 1
            print(f"CUSTOMER {i} has entered the waiting room, SEATS occupied: {shared.waiting_room}")
            shared.customer.signal()  # signal to wake up barber, customer ready for haircut
            shared.mutex.unlock()
            shared.barber.wait()  # wait for barber to signal customer
            get_haircut(i)
            shared.customer_done.signal()  # signal barber when done
            print(f"CUSTOMER {i} is DONE getting a haircut and LEAVING")
            growing_hair(i)
            shared.barber_done.wait()  # wait for barber to signal customer when they are done

        else:
            shared.mutex.unlock()
            balk(i)


def barber(shared):
    """Simulates barbers behavior
    Arguments:
        shared -- object of class Shared
    """
    while True:
        shared.customer.wait()  # wait for customer signal
        shared.mutex.lock()
        shared.waiting_room -= 1
        shared.mutex.unlock()
        shared.barber.signal()  # signal customer that they are ready
        cut_hair()
        shared.customer_done.wait()  # wait for customer signal
        print(f"\nBARBER is DONE cutting hair\n")
        shared.barber_done.signal()  # signal customer that barber is done


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

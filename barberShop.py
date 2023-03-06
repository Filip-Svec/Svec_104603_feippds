""" Program represents different sequences of using mutex

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Marián Šebeňa"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, print, Semaphore
from time import sleep
from random import randint


class Shared(object):

    def __init__(self):
        # TODO : Initialize patterns we need and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    print("CUSTOMER ", i, " is getting a hair cut")
    sleep(randint(1, 3))


def cut_hair():
    print("BARBER is cutting hair")
    sleep(randint(1, 3))


def balk(i):
    print("CUSTOMER ", i, " is waiting, room is full")
    sleep(randint(1, 3))


def growing_hair(i):
    sleep(randint(1, 3))


def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)

        # TODO: Rendezvous 1
        get_haircut(i)
        # TODO: Rendezvous 2

        # TODO: Leave waiting room. Integrity again
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


# TODO: Global variables C = 5 numOfCustomers N = 3 sizeOfWaitingRoom
C = 5
N = 3

if __name__ == "__main__":
    main()

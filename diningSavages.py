"""This module implements dinning savages problem.

This implementation of the dining savages problem
utilizes more than one cook.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Filip Švec, Tomáš Vavro, Marián Šebeňa"
__email__ = "xsvecf@stuba.sk, xvavro@stuba.sk, mariansebena@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Semaphore, Mutex, print
from time import sleep

NUM_SAVAGES = 5
NUM_COOKS = 4
NUM_PORTIONS_POT = 3


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""

        self.mutex_enter_kitchen = Mutex()  # only one savage in the kitchen
        self.mutex_accessing_pot = Mutex()  # only one savage / cook accessing the pot
        self.mutexCountSavages = Mutex()
        self.mutexCountCooks = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.turnstile_1_start = Semaphore(0)   # savage barrier
        self.turnstile_2_end = Semaphore(0)     # savage barrier
        self.turnstile_3_cook = Semaphore(0)    # cook barrier
        self.turnstile_4_cook = Semaphore(0)    # cook barrier

        self.countSavages = 0
        self.countCooks = 0
        self.portions_left = NUM_PORTIONS_POT


def savage(i, shared):
    """Run savage's process.

    Args:
        i -- thread number (id)
        shared -- shared data
    """
    while True:

        # Wait for all other savages to finish eating before getting more food
        shared.mutexCountSavages.lock()
        shared.countSavages += 1
        if shared.countSavages == NUM_SAVAGES:
            shared.turnstile_1_start.signal(NUM_SAVAGES)
            print(f'Savage {i} signals to eat. Count savages = {shared.countSavages} / {NUM_SAVAGES} \n')
        else:
            print(f'Savage {i} is waiting. Count savages = {shared.countSavages} / {NUM_SAVAGES}')
        shared.mutexCountSavages.unlock()
        shared.turnstile_1_start.wait()

        # Lock the whole process (kitchen for savages), only one will enter
        shared.mutex_enter_kitchen.lock()

        # Savage in the kitchen locks access to the pot
        shared.mutex_accessing_pot.lock()

        # Check for empty pot
        if shared.portions_left == 0:

            # Signal cook that pot is empty and unlock access to the pot
            shared.full_pot.signal(NUM_COOKS)
            shared.mutex_accessing_pot.unlock()

            # Savage waits in the kitchen until cooks are done
            print(f"Savage {i} signals cook that pot is empty and waits! \n")
            shared.empty_pot.wait()

            # Cooks are done, savage in the kitchen can take his portion
            shared.mutex_accessing_pot.lock()
            shared.portions_left -= 1
            print(f"Savage {i} took portion! Portions left: {shared.portions_left} / {NUM_PORTIONS_POT}")
            shared.mutex_accessing_pot.unlock()
        else:
            shared.portions_left -= 1
            print(f"Savage {i} took portion! Portions left: {shared.portions_left} / {NUM_PORTIONS_POT}")
            shared.mutex_accessing_pot.unlock()

        # Another savage can enter chicken
        shared.mutex_enter_kitchen.unlock()

        # Savage is eating
        print(f"Savage {i} is eating!")
        sleep(0.5)

        # Reusable barrier second part
        shared.mutexCountSavages.lock()
        shared.countSavages -= 1
        if shared.countSavages == 0:
            print(f"Every savage has eaten. Ah #$@1, here we go again.\n")
            shared.turnstile_2_end.signal(NUM_SAVAGES)
        shared.mutexCountSavages.unlock()
        shared.turnstile_2_end.wait()


def cook(i, shared):
    """Run cook's process.

    Args:
        shared -- shared data
        i -- thread number (id)
    """
    while True:

        # Wait for savages to signal that pot is empty
        shared.full_pot.wait()

        while True:

            # Cook accessing the pot (adding portion)
            shared.mutex_accessing_pot.lock()
            if shared.portions_left == NUM_PORTIONS_POT:
                shared.mutex_accessing_pot.unlock()
                break
            else:
                shared.portions_left += 1
                print(f"Cook {i} added a portion! Portions left: {shared.portions_left} / {NUM_PORTIONS_POT}")
                shared.mutex_accessing_pot.unlock()
                sleep(0.2)

        # Reusable barrier so that all cooks leave kitchen and the last one signals that the pot is full
        shared.mutexCountCooks.lock()
        shared.countCooks += 1
        if shared.countCooks == NUM_COOKS:
            print(f'Cook {i} signals to leave kitchen. Savages EAT! Count cooks = {shared.countCooks} / {NUM_COOKS} \n')
            shared.turnstile_3_cook.signal(NUM_COOKS)
        else:
            print(f'Cook {i} is waiting. Count cooks = {shared.countCooks} / {NUM_COOKS}')
        shared.mutexCountCooks.unlock()
        shared.turnstile_3_cook.wait()

        shared.mutexCountCooks.lock()
        shared.countCooks -= 1
        if shared.countCooks == 0:
            shared.empty_pot.signal()    # Signal that pot is full again
            shared.turnstile_4_cook.signal(NUM_COOKS)
        shared.mutexCountCooks.unlock()
        shared.turnstile_4_cook.wait()


def main():
    """Run main."""

    shared = Shared()
    savages = [
        Thread(savage, i, shared) for i in range(NUM_SAVAGES)
    ]
    cooks = [
        Thread(cook, i, shared) for i in range(NUM_COOKS)
    ]

    for s in savages:
        s.join()

    for c in cooks:
        c.join()


if __name__ == "__main__":
    main()

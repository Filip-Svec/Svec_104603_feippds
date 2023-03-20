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
        self.turnstile_1_start = Semaphore(0)
        self.turnstile_2_end = Semaphore(0)
        self.turnstile_3_cook = Semaphore(0)
        self.turnstile_4_cook = Semaphore(0)

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
        # pravdepodobne tu bude chyba skusit spravit taku simple barieru a ten count-
        # -len modulovat poctom savages tak aby ich pustilo len ked tam budu vsetcia

        # shared.mutexCountSavages.lock()
        # shared.countSavages += 1
        # if shared.countSavages == NUM_SAVAGES:
        #     print(f'Savage {i} signals to eat. Count = {shared.countSavages}')
        #     shared.turnstile_1_start.signal(NUM_SAVAGES)
        #     shared.mutexCountSavages.unlock()
        # else:
        #     print(f'Savage {i} is waiting. Count = {shared.countSavages}')
        #     shared.mutexCountSavages.unlock()
        #     shared.turnstile_1_start.wait()

        shared.mutexCountSavages.lock()
        shared.countSavages += 1
        if shared.countSavages == NUM_SAVAGES:
            shared.turnstile_1_start.signal(NUM_SAVAGES)
            print(f'Savage {i} signals to eat. Count = {shared.countSavages}')
        shared.mutexCountSavages.unlock()
        shared.turnstile_1_start.wait()

        # Lock the whole process
        shared.mutex_enter_kitchen.lock()

        # Take portion
        shared.mutex_accessing_pot.lock()
        # Check for empty pot
        if shared.portions_left == 0:
            shared.full_pot.signal(NUM_COOKS)  # Signal cook that pot is empty
            print(f"Savage {i} signals cook that pot is empty and waits!")
            shared.mutex_accessing_pot.unlock()
            shared.empty_pot.wait()
            shared.mutex_accessing_pot.lock()
            shared.portions_left -= 1
            print(f"Savage {i} is eating! Portions left: {shared.portions_left}")
            shared.mutex_accessing_pot.unlock()
        else:
            shared.portions_left -= 1
            print(f"Savage {i} is eating! Portions left: {shared.portions_left} Count = {shared.countSavages}")
            shared.mutex_accessing_pot.unlock()

        shared.mutex_enter_kitchen.unlock()

        # Simulate eating
        sleep(0.5)

        # shared.mutexCountSavages.lock()
        # shared.countSavages -= 1
        # if shared.countSavages == 0:
        #     shared.turnstile_2_end.signal(NUM_SAVAGES-1)
        #     print(f'Savage {i} signals to release barrier. Count = {shared.countSavages}')
        #     shared.mutexCountSavages.unlock()
        # else:
        #     shared.mutexCountSavages.unlock()
        #     print(f'Savage {i} is waiting on barrier. Count = {shared.countSavages}')
        #     shared.turnstile_2_end.wait()

        shared.mutexCountSavages.lock()
        shared.countSavages -= 1
        if shared.countSavages == 0:
            shared.turnstile_2_end.signal(NUM_SAVAGES)
            print(f'Savage {i} signals to release barrier. Count = {shared.countSavages}')
        shared.mutexCountSavages.unlock()
        shared.turnstile_2_end.wait()


def cook(i, shared):
    """Run cook's process.

    Args:
        shared -- shared data
        i -- thread number (id)
    """

    # Wait for pot to be empty
    print(f'Cook {i} is waiting for Empty pot signal')
    shared.full_pot.wait()

    while True:
        # Cook portion
        shared.mutex_accessing_pot.lock()
        if shared.portions_left == NUM_PORTIONS_POT:
            # Signal that pot is full again
            shared.mutex_accessing_pot.unlock()
            break
        else:
            shared.portions_left += 1
            print(f"Cook {i} cooked a portion! Portions left: {shared.portions_left}")
            shared.mutex_accessing_pot.unlock()
            sleep(0.2)

    # barrier so that all cooks leave kitchen and the last one signals that the pot is full
    shared.mutexCountCooks.lock()
    shared.countCooks += 1
    if shared.countCooks == NUM_COOKS:
        print(f'Cook {i} signals to leave kitchen. POT is FULL.')
        shared.turnstile_3_cook.signal(NUM_COOKS)
        shared.empty_pot.signal()
    else:
        print(f'Cook {i} is waiting for all the cooks to finish.')
    shared.mutexCountCooks.unlock()
    shared.turnstile_3_cook.wait()

    shared.mutexCountCooks.lock()
    shared.countCooks -= 1
    if shared.countCooks == 0:
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


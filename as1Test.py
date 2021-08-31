import numpy
import math
import random


# Generate 100 random integers in [10, 50] and add them into a
# queue − Process the queue so that only unique numbers are printed on the screen
def addtoQueue(count, min, max):
    count = 0
    while count >= 0:
        temp = random.randint(min, max)
        uniqueNums(temp)
        count - 1


def uniqueNums(queue):
    unique = []
    exists = queue in unique
    if exists == False:
        unique.append(queue)
    else:
        print(f"Value {queue} is already in the array")
    return unique


if __name__ == "__main__":
    addtoQueue(100, 10, 50)

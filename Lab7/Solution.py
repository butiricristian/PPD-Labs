from multiprocessing.pool import ThreadPool
from random import random

import math
from threading import Thread, Lock

from copy import deepcopy

inputList = []
outputList = []
l = Lock()


def firstPass(begin, end):
    if begin == end:
        return inputList[begin]
    tp = ThreadPool(1)
    mid = (begin + end) // 2
    t1 = tp.apply_async(func=firstPass, args=(begin, mid)).get()
    t2 = tp.apply_async(func=firstPass, args=(mid + 1, end)).get()
    # t1 = firstPass(begin, mid)
    # t2 = firstPass(mid + 1, end)
    outputList[end] = t1 + t2
    return t1 + t2


def secondPass(begin, end):
    if begin == end:
        return
    mid = (begin + end) // 2
    l.acquire()
    tmp = outputList[mid]
    outputList[mid] = outputList[end]
    outputList[end] += tmp
    l.release()
    t1 = Thread(target=secondPass, args=(begin, mid))
    t2 = Thread(target=secondPass, args=(mid+1, end))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # secondPass(begin, mid)
    # secondPass(mid + 1, end)


def main():
    global inputList
    global outputList

    size = 16
    inputList = [x + 1 for x in range(size)]
    outputList = deepcopy(inputList)

    firstPass(0, size - 1)
    print(outputList)
    tmp = outputList[size - 1]
    outputList[size - 1] = 0
    secondPass(0, size - 1)
    outputList.append(tmp)

    print(inputList)
    print(outputList)


main()

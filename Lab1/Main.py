import datetime
import threading
from timeit import default_timer as timer

import numpy as np

res = []


def work_split(nrTasks, nrWorkers):
    return (nrTasks // nrWorkers, nrTasks % nrWorkers)


def user_input():
    nrWorkers = int(input("Number of workers: "))
    N = int(input("N= "))
    K = int(input("K= "))
    M = int(input("M= "))
    global res
    res = [[0 for _ in range(N)] for _ in range(M)]
    solve(nrWorkers, N, K, M)


def worker(matrix1, matrix2, a, b):
    res[a:b] = np.dot(matrix1[a:b], matrix2)


def solve(nrWorkers, N, K, M):
    matrix1 = np.random.random_integers(100, size=(N, K))
    matrix2 = np.random.random_integers(100, size=(K, M))
    interval, rest = work_split(N, nrWorkers)
    threads = []

    start1 = timer()
    res2 = np.dot(matrix1, matrix2)
    end1 = timer()

    start2 = timer()
    for i in range(nrWorkers - 1):
        if rest > 0:
            t = threading.Thread(target=worker, args=(matrix1, matrix2, i * (interval + 1), (i + 1) * (interval + 1)))
            threads.append(t)
            t.start()
            rest -= 1
        t = threading.Thread(target=worker, args=(matrix1, matrix2, i * interval, (i + 1) * interval))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end2 = timer()

    print("Without threads: ", end1 - start1)
    print("With threads: ", end2 - start2)


user_input()

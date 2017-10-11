import threading

import numpy as np

res = []

def work_split(nrTasks, nrWorkers):
    return (nrTasks / nrWorkers, nrTasks % nrWorkers)


def user_input():
    nrWorkers = int(input("Number of workers: "))
    N = int(input("N= "))
    K = int(input("K= "))
    M = int(input("M= "))
    global res
    res = [[0 for _ in range(N)] for _ in range(M)]


def worker(matrix1, matrix2, a, b):
    res[a:b] = np.dot(matrix1[a:b], matrix2)


def solve(nrWorkers, N, K, M):
    matrix1 = np.random.random_integers(100, size=(N, K))
    matrix2 = np.random.random_integers(100, size=(K, M))
    print(matrix1, "\n", matrix2)
    interval, lastInterval = work_split(N, nrWorkers)
    threads = []
    for i in range(nrWorkers - 1):
        t = threading.Thread(target=worker, args=(matrix1, matrix2, i * interval, (i + 1) * interval))
        threads.append(t)
        t.start()
    t = threading.Thread(target=np.dot,
                         args=(matrix1[(nrWorkers - 1) * interval:(nrWorkers - 1) * interval + lastInterval], matrix2))
    threads.append(t)
    t.start()

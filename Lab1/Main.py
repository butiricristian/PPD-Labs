import numpy as np


def work_split(nrTasks, nrWorkers):
    return (nrTasks/nrWorkers, nrTasks%nrWorkers)


def user_input():
    nrWorkers = int(input("Number of workers: "))
    N = int(input("N= "))
    K = int(input("K= "))
    M = int(input("M= "))


def solve(nrWorkers, N, K, M):
    matrix1 = np.random.random_integers(100, size=(N, K))
    matrix2 = np.random.random_integers(100, size=(K, M))
    print(matrix1, "\n", matrix2)
    interval, lastInterval = work_split(N, nrWorkers)

    for i in range(nrWorkers):
        res = np.dot(matrix1[i:(i+interval)], matrix2)




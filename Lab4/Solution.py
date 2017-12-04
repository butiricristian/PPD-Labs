import time
import threading
from timeit import default_timer as timer

import numpy as np

tmpRes = []
finRes = []
condition = threading.Condition()
N, K, M, P = (0, 0, 0, 0)


def work_split(nrTasks, nrWorkers):
    return (nrTasks // nrWorkers, nrTasks % nrWorkers)


def user_input():
    nrWorkers = int(input("Number of workers: "))
    global N, K, M, P
    N = int(input("N= "))
    K = int(input("K= "))
    M = int(input("M= "))
    P = int(input("P= "))
    global finRes
    global tmpRes
    tmpRes = [[0 for _ in range(M)] for _ in range(N)]
    finRes = [[0 for _ in range(P)] for _ in range(N)]
    solve(nrWorkers)


def producer(matrix1, matrix2, a, b):
    condition.acquire()
    tmpRes[a:b] = np.dot(matrix1[a:b], matrix2)
    print("Produced lines: " + str(a) + "->" + str(b))
    condition.notify_all()
    condition.release()


def consumer(matrix3, a, b):
    while True:
        condition.acquire()
        if tmpRes[a:b] == [[0 for _ in range(M)] for _ in range(b-a)]:
            condition.wait()
        finRes[a:b] = np.dot(tmpRes[a:b], matrix3)
        print("Consumed lines: " + str(a) + "->" + str(b))
        condition.release()
        break


def solve(nrWorkers):
    global N, K, M, P
    matrix1 = np.random.random_integers(10, size=(N, K))
    matrix2 = np.random.random_integers(10, size=(K, M))
    matrix3 = np.random.random_integers(10, size=(M, P))
    interval, rest = work_split(N, nrWorkers)
    aux = rest
    threads = []

    start1 = timer()
    res2 = np.dot(matrix1, matrix2)
    res3 = np.dot(res2, matrix3)
    end1 = timer()

    start2 = timer()
    for i in range(nrWorkers):
        if aux > 0:
            t1 = threading.Thread(target=producer, args=(matrix1, matrix2, i * (interval + 1), (i + 1) * (interval + 1)))
            t2 = threading.Thread(target=consumer, args=(matrix3, i * (interval + 1), (i + 1) * (interval + 1)))
            threads.append(t1)
            threads.append(t2)
            t2.start()
            t1.start()
            aux -= 1
        else:
            t1 = threading.Thread(target=producer, args=(matrix1, matrix2, i * interval + rest, (i + 1) * interval + rest))
            t2 = threading.Thread(target=consumer, args=(matrix3, i * interval + rest, (i + 1) * interval + rest))
            threads.append(t1)
            threads.append(t2)
            t2.start()
            t1.start()

    for t in threads:
        t.join()
    end2 = timer()

    # for i in range(N):
    #     for j in range(P):
    #         if finRes[i][j] != res3[i][j]:
    #             print("FALSE")

    print(res3)
    print()
    print(finRes)

    print("Without threads: ", end1 - start1)
    print("With threads: ", end2 - start2)


user_input()

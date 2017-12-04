# (4x^3+2x^2+3x+1)
from datetime import datetime
from random import random
from threading import Thread, Lock
from multiprocessing.pool import ThreadPool

from numpy.polynomial import Polynomial


m = Lock()



def gradeSchoolSeq(poly1, poly2):
    pRes = Polynomial([0 for _ in range(len(poly1.coef)+len(poly2.coef)-1)])
    for x in range(len(poly1.coef)):
        for y in range(len(poly2.coef)):
            pRes.coef[x+y] += poly1.coef[x] * poly2.coef[y]
    return pRes


def singleMultiplication(poly1, poly2, pRes, begin, end):
    for x in range(begin, end):
        for y in range(len(poly2.coef)):
            m.acquire()
            pRes.coef[x+y] += poly1.coef[x]*poly2.coef[y]
            m.release()

def gradeSchoolParallel(poly1, poly2):
    pRes = Polynomial([0 for _ in range(len(poly1.coef) + len(poly2.coef) - 1)])
    nrWorkers = 4
    step = len(poly1.coef)//nrWorkers
    stepRemainder = len(poly1.coef)%nrWorkers
    threads = []
    for x in range(nrWorkers):
        if stepRemainder != 0:
            t = Thread(target=singleMultiplication, args=(poly1, poly2, pRes, x*(step+1), (x+1)*(step+1)))
            stepRemainder -= 1
        else:
            t = Thread(target=singleMultiplication, args=(poly1, poly2, pRes, x*step + len(poly1.coef)%nrWorkers,
                                                          (x+1)*step + len(poly1.coef)%nrWorkers))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return pRes


def karatsubaThreaded(poly1, poly2):
    threshold = 20
    if poly1.degree() <= threshold or poly2.degree() <= threshold:
        return gradeSchoolSeq(poly1, poly2)

    mid = max(len(poly1.coef), len(poly2.coef))//2

    low1 = Polynomial(poly1.coef[:mid])
    low2 = Polynomial(poly2.coef[:mid])
    high1 = Polynomial(poly1.coef[mid:])
    high2 = Polynomial(poly2.coef[mid:])

    tp = ThreadPool(processes=3)
    res1 = tp.apply_async(func=karatsubaThreaded, args=(low1, low2)).get()
    res2 = tp.apply_async(func=karatsubaThreaded, args=(low1+high1, low2+high2)).get()
    res3 = tp.apply_async(func=karatsubaThreaded, args=(high1, high2)).get()

    return gradeSchoolSeq(res3, Polynomial([1] + [0 for _ in range(2*mid)])) + \
        gradeSchoolSeq((res2 - res1 - res3), Polynomial([1] + [0 for _ in range(mid)])) + \
        res1

def karatsubaSeq(poly1, poly2):
    threshold = 20
    if poly1.degree() <= threshold or poly2.degree() <= threshold:
        return gradeSchoolSeq(poly1, poly2)

    mid = max(len(poly1.coef), len(poly2.coef)) // 2

    low1 = Polynomial(poly1.coef[:mid])
    low2 = Polynomial(poly2.coef[:mid])
    high1 = Polynomial(poly1.coef[mid:])
    high2 = Polynomial(poly2.coef[mid:])

    res1 = karatsubaThreaded(low1, low2)
    res2 = karatsubaThreaded(low1 + high1, low2 + high2)
    res3 = karatsubaThreaded(high1, high2)

    return gradeSchoolSeq(res3, Polynomial([1] + [0 for _ in range(2 * mid)])) + \
           gradeSchoolSeq((res2 - res1 - res3), Polynomial([1] + [0 for _ in range(mid)])) + \
           res1

def main():
    deg1 = 1000
    deg2 = 1000
    poly1 = Polynomial([int(random()*100) for _ in range(deg1)])
    poly2 = Polynomial([int(random()*100) for _ in range(deg2)])
    # poly1 = Polynomial([4, 2, 1, 3, 6])
    # poly2 = Polynomial([10, 2, 5, 3, 1])
    t1 = datetime.now()
    gradeSchoolSeq(poly1, poly2)
    t2 = datetime.now()
    gradeSchoolParallel(poly1, poly2)
    t3 = datetime.now()
    karatsubaSeq(poly1, poly2)
    t4 = datetime.now()
    karatsubaThreaded(poly1, poly2)
    t5 = datetime.now()
    print("Normal sequential: ", (t2 - t1).microseconds)
    print("Normal parallel", (t3 - t2).microseconds)
    print("Karatsuba sequential", (t4 - t3).microseconds)
    print("Karatsuba parallel", (t5 - t4).microseconds)
    # print(gradeSchoolSeq(poly1, poly2))
    # print(gradeSchoolParallel(poly1, poly2))
    # print(karatsubaSeq(poly1, poly2))
    # print(karatsubaThreaded(poly1, poly2))

main()

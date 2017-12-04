from multiprocessing.pool import ThreadPool
from random import Random
from threading import Thread, Lock

l = Lock()
seed = 100000
adj = []
n = 6
m = 0


def worker():
    global seed
    global adj
    l.acquire()
    r = Random()
    r.seed(seed)
    seed += 100000
    l.release()
    for i in range(100000):
        res = True
        nodes = []
        for x in range(n):
            nodes.append(x)
        r.shuffle(nodes)
        for i in range(len(nodes)):
            if not adj[nodes[i]][nodes[(i + 1) % n]] is True:
                res = False
        if res is True:
            print("True")
            return


def main():
    global adj, n, m
    adj = [[False for _ in range(n)] for _ in range(n)]
    r = Random()
    m = r.randint(int(0.9 * (n*(n-1))), n*(n-1))
    # m = 1
    while m > 0:
        start = r.randint(0, n-1)
        end = r.randint(0, n-1)
        if start != end and not adj[start][end]:
            adj[start][end] = True
            m -= 1
    threads = []
    for i in range(10):
        t = Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

main()

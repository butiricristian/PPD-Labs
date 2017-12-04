from queue import Queue
from threading import Thread

numbers = []


def multiply(i1, i2, res):
    if i1 == i2:
        for c in numbers[i1]:
            res.put(c)
        res.put(None)
        return
    if i1 == i2 - 1:
        carry = 0
        len1 = len(numbers[i1])
        len2 = len(numbers[i2])
        minLength = min(len1, len2)
        for i in range(minLength):
            tmp = numbers[i1][i] + numbers[i2][i] + carry
            res.put(tmp % 10)
            carry = tmp // 10
        for i in range(len1 - len2):
            tmp = numbers[i1][i + len2] + carry
            res.put(tmp % 10)
            carry = tmp // 10
        for i in range(len2 - len1):
            tmp = numbers[i2][i + len1] + carry
            res.put(tmp % 10)
            carry = tmp // 10
        if carry == 1:
            res.put(carry)
        res.put(None)
        return

    mid = (i1 + i2) // 2
    queue1 = Queue()
    queue2 = Queue()
    t1 = Thread(target=multiply, args=(i1, mid, queue1))
    t2 = Thread(target=multiply, args=(mid + 1, i2, queue2))
    t1.start()
    t2.start()
    # multiply(i1, mid, queue1)
    # multiply(mid+1, i2, queue2)
    carry = 0
    while True:
        c1 = queue1.get()
        c2 = queue2.get()
        if c1 is None:
            while not c2 is None:
                tmp = c2 + carry
                res.put(tmp % 10)
                carry = tmp // 10
                c2 = queue2.get()
            t1.join()
            t2.join()
            if carry == 1:
                res.put(carry)
            res.put(None)
            return
        elif c2 is None:
            while not c1 is None:
                tmp = c1 + carry
                res.put(tmp % 10)
                carry = tmp // 10
                c1 = queue1.get()
            t1.join()
            t2.join()
            if carry == 1:
                res.put(carry)
            res.put(None)
            return
        else:
            tmp = c1 + c2 + carry
            res.put(tmp % 10)
            carry = tmp // 10


def main():
    global numbers
    inputNumbers = ["18300185877878983000", "94111802487705630000", "43506089492427090", "18980939942703710000", "43244811007774260000", "43608238829313820000", "54051738540040616"]
    for i in range(len(inputNumbers)):
        nrLen = len(inputNumbers[i])
        numbers.append([None for _ in range(nrLen)])
        for j in range(nrLen):
            numbers[i][nrLen - j - 1] = int(inputNumbers[i][j])
    res = Queue()
    multiply(0, len(numbers)-1, res)
    finalRes = []
    while not res.empty():
        x = res.get()
        if not x is None:
            finalRes.append(x)
    for c in reversed(finalRes):
        print(c, end="")


main()

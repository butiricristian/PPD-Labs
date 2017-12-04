import threading
import time

from Operation import Operation
from Transfer import Transfer
from Account import Account

accounts = {1: Account(1, 300001, []), 2: Account(2, 1, [])}
lock = threading.Lock()


def transfer_op(operation):
    for transfer in operation.transfers:
        with lock:
            accounts[transfer.accountId1].amount -= transfer.value
            accounts[transfer.accountId1].log.append(transfer)
            accounts[transfer.accountId2].amount += transfer.value
            accounts[transfer.accountId2].log.append(transfer)


def check():
    while True:
        for acc in accounts:
            print(str(accounts[acc]))
        print()
        time.sleep(0.001)
        if threading.active_count() == 2:
            break


def bank():
    threads = []
    operations = []
    for y in range(3):
        operations.append(Operation([Transfer(x + y * 10, 1, 2, 1) for x in range(100000)]))

    tCheck = threading.Thread(target=check)
    tCheck.start()
    threads.append(tCheck)

    for operation in operations:
        t = threading.Thread(target=transfer_op, args=[operation])
        t.daemon = True
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for acc in accounts:
        print(str(accounts[acc]))


bank()

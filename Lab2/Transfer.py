class Transfer:
    def __init__(self, id, account_id1, account_id2, value):
        self.id = id
        self.accountId1 = account_id1
        self.accountId2 = account_id2
        self.value = value

    def __str__(self):
        return "Transfer: " + str(self.id) + ", " + str(self.accountId1) + "->" + str(self.accountId2) + " = " + str(self.value)

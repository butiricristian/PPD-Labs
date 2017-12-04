class Account:
    def __init__(self, id, amount, log_entries):
        self.id = id
        self.amount = amount
        self.log = log_entries

    def __str__(self):
        ret = "Account: " + str(self.id) + ", " + str(self.amount)
        return ret

    def full_str(self):
        ret = "Account: " + str(self.id) + ", " + str(self.amount) + ", logs = {"
        for l in self.log:
            ret += str(l) + "\n"
        ret += " }"
        return ret

import json
from storage.base_storage import BaseStorage

class JSONStorage(BaseStorage):
    def __init__(self, filename="data/data.json"):
        self.filename = filename
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except:
            self.data = {}

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def create_account(self, account):
        self.data[account["account_no"]] = account
        self.save()

    def get_account(self, account_no):
        return self.data.get(account_no)

    def update_account(self, account_no, updated):
        self.data[account_no].update(updated)
        self.save()

    def delete_account(self, account_no):
        self.data.pop(account_no, None)
        self.save()

    def deposit(self, account_no, amount):
        self.data[account_no]["balance"] += amount
        self.save()

    def withdraw(self, account_no, amount):
        if self.data[account_no]["balance"] >= amount:
            self.data[account_no]["balance"] -= amount
            self.save()
            return True
        return False

    def list_customers(self):
        return list(self.data.values())

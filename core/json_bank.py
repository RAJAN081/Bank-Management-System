import json
from pathlib import Path

class JSONBank:
    database = "data/data.json"

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, "r") as f:
                return json.load(f)
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def generate_acc(cls):
        import random, string
        chars = random.choices(string.ascii_letters, k=3) + \
                random.choices(string.digits, k=3)
        random.shuffle(chars)
        return "".join(chars)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return None, "Age must be 18+ and PIN must be 4 digits"

        data = cls.load_data()
        acc = cls.generate_acc()

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": acc,
            "balance": 0
        }

        data.append(user)
        cls.save_data(data)
        return user, "Account created"

    @classmethod
    def find_user(cls, acc, pin):
        data = cls.load_data()
        for u in data:
            if u["accountNo"] == acc and u["pin"] == pin:
                return u
        return None

    @classmethod
    def deposit(cls, acc, pin, amount):
        data = cls.load_data()
        for u in data:
            if u["accountNo"] == acc and u["pin"] == pin:
                u["balance"] += amount
                cls.save_data(data)
                return True, "Deposit successful"
        return False, "Invalid account / pin"

    @classmethod
    def withdraw(cls, acc, pin, amount):
        data = cls.load_data()
        for u in data:
            if u["accountNo"] == acc and u["pin"] == pin:
                if u["balance"] >= amount:
                    u["balance"] -= amount
                    cls.save_data(data)
                    return True, "Withdraw successful"
                return False, "Not enough balance"
        return False, "Invalid account"

    @classmethod
    def update(cls, acc, pin, name=None, email=None, new_pin=None):
        data = cls.load_data()
        for u in data:
            if u["accountNo"] == acc and u["pin"] == pin:
                if name: u["name"] = name
                if email: u["email"] = email
                if new_pin: u["pin"] = int(new_pin)
                cls.save_data(data)
                return True, "Updated"
        return False, "User not found"

    @classmethod
    def delete(cls, acc, pin):
        data = cls.load_data()
        for i, u in enumerate(data):
            if u["accountNo"] == acc and u["pin"] == pin:
                data.pop(i)
                cls.save_data(data)
                return True, "Deleted"
        return False, "User not found"

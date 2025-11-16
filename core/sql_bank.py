import sqlite3

class SQLBank:
    db = "database/bank.db"

    @classmethod
    def connect(cls):
        return sqlite3.connect(cls.db)

    @classmethod
    def setup(cls):
        conn = cls.connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                name TEXT,
                age INT,
                email TEXT,
                pin INT,
                accountNo TEXT PRIMARY KEY,
                balance INT
            )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return None, "Age must be 18+ and PIN must be 4 digits"

        import random, string
        acc = "".join(random.choices(string.ascii_letters + string.digits, k=6))

        conn = cls.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                    (name, age, email, pin, acc, 0))
        conn.commit()
        conn.close()

        return {"name": name, "age": age, "email": email, "pin": pin, "accountNo": acc, "balance": 0}, \
               "Account created"

    @classmethod
    def find_user(cls, acc, pin):
        conn = cls.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE accountNo=? AND pin=?", (acc, pin))
        row = cur.fetchone()
        conn.close()
        return row

    @classmethod
    def deposit(cls, acc, pin, amt):
        conn = cls.connect()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE accountNo=? AND pin=?", (acc, pin))
        row = cur.fetchone()

        if not row:
            return False, "Invalid account"

        new_balance = row[0] + amt
        cur.execute("UPDATE users SET balance=? WHERE accountNo=?", (new_balance, acc))

        conn.commit()
        conn.close()
        return True, "Deposit successful"

    @classmethod
    def withdraw(cls, acc, pin, amt):
        conn = cls.connect()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE accountNo=? AND pin=?", (acc, pin))
        row = cur.fetchone()

        if not row:
            return False, "Invalid account"

        if row[0] < amt:
            return False, "Not enough balance"

        new_balance = row[0] - amt
        cur.execute("UPDATE users SET balance=? WHERE accountNo=?", (new_balance, acc))

        conn.commit()
        conn.close()
        return True, "Withdraw successful"

    @classmethod
    def delete(cls, acc, pin):
        conn = cls.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE accountNo=? AND pin=?", (acc, pin))
        conn.commit()
        conn.close()
        return True, "Deleted"

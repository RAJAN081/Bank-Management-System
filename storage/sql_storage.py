import sqlite3
from storage.base_storage import BaseStorage

class SQLStorage(BaseStorage):
    def __init__(self, db="database/bank.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
                account_no TEXT PRIMARY KEY,
                name TEXT,
                balance INTEGER
            )
        """)
        self.conn.commit()

    def create_account(self, account):
        self.cur.execute(
            "INSERT INTO accounts VALUES (?, ?, ?)",
            (account["account_no"], account["name"], account["balance"])
        )
        self.conn.commit()

    def get_account(self, account_no):
        row = self.cur.execute(
            "SELECT * FROM accounts WHERE account_no=?",
            (account_no,)
        ).fetchone()

        if row:
            return {"account_no": row[0], "name": row[1], "balance": row[2]}
        return None

    def update_account(self, account_no, updated):
        for key, value in updated.items():
            self.cur.execute(
                f"UPDATE accounts SET {key}=? WHERE account_no=?",
                (value, account_no)
            )
        self.conn.commit()

    def delete_account(self, account_no):
        self.cur.execute("DELETE FROM accounts WHERE account_no=?", (account_no,))
        self.conn.commit()

    def deposit(self, account_no, amount):
        self.cur.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_no=?",
            (amount, account_no)
        )
        self.conn.commit()

    def withdraw(self, account_no, amount):
        acc = self.get_account(account_no)
        if acc and acc["balance"] >= amount:
            self.cur.execute(
                "UPDATE accounts SET balance = balance - ? WHERE account_no=?",
                (amount, account_no)
            )
            self.conn.commit()
            return True
        return False

    def list_customers(self):
        rows = self.cur.execute("SELECT * FROM accounts").fetchall()
        return [{"account_no": r[0], "name": r[1], "balance": r[2]} for r in rows]

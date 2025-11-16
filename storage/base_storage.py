class BaseStorage:
    def create_account(self, account): pass
    def get_account(self, account_no): pass
    def update_account(self, account_no, data): pass
    def delete_account(self, account_no): pass
    def deposit(self, account_no, amount): pass
    def withdraw(self, account_no, amount): pass
    def list_customers(self): pass
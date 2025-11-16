import streamlit as st
from core.json_bank import JSONBank
from core.sql_bank import SQLBank

st.set_page_config(page_title="Bank App", layout="centered")
st.title("🏦 Bank Management System")

# Setup SQL table on first run
SQLBank.setup()

# Choose backend
backend = st.sidebar.radio("Choose Storage", ["JSON", "SQL"])

if backend == "JSON":
    Bank = JSONBank
else:
    Bank = SQLBank

menu = st.sidebar.selectbox("Choose Action",
    ["Create Account", "Deposit", "Withdraw", "Show Details",
     "Update Info", "Delete Account"])

# ---- Create Account ----
if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create"):
        if not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be 4 digits")
        else:
            user, msg = Bank.create_account(name, int(age), email, int(pin))
            st.success(msg)
            if user:
                st.info(f"Your Account Number: {user['accountNo']}")

# ---- Deposit ----
elif menu == "Deposit":
    st.subheader("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        ok, msg = Bank.deposit(acc, int(pin), int(amt))
        st.success(msg) if ok else st.error(msg)

# ---- Withdraw ----
elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        ok, msg = Bank.withdraw(acc, int(pin), int(amt))
        st.success(msg) if ok else st.error(msg)

# ---- Show Details ----
elif menu == "Show Details":
    st.subheader("View Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        user = Bank.find_user(acc, int(pin))
        if user:
            st.json({
                "name": user[0] if backend == "SQL" else user["name"],
                "age": user[1] if backend == "SQL" else user["age"],
                "email": user[2] if backend == "SQL" else user["email"],
                "pin": user[3] if backend == "SQL" else user["pin"],
                "accountNo": user[4] if backend == "SQL" else user["accountNo"],
                "balance": user[5] if backend == "SQL" else user["balance"],
            })
        else:
            st.error("Account not found")

# ---- Update Info ----
elif menu == "Update Info":
    st.subheader("Update Info")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_pin = st.text_input("New PIN")

    if st.button("Update"):
        ok, msg = Bank.update(acc, int(pin), new_name, new_email, new_pin)
        st.success(msg) if ok else st.error(msg)

# ---- Delete Account ----
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        ok, msg = Bank.delete(acc, int(pin))
        st.success(msg) if ok else st.error(msg)

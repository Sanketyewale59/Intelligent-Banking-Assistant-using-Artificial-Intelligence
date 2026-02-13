import os


def load_db():
    db = {}
    with open("database.txt", "r") as f:
        for line in f:
            if ":" in line:          # ignore bad lines
                k, v = line.strip().split(":", 1)
                db[k] = v
    return db


def get_customer():
    if os.path.exists("customers.txt"):
        with open("customers.txt", "r") as f:
            return f.read().strip()
    return ""

def save_customer(name):
    with open("customers.txt", "w") as f:
        f.write(name)


def log_transaction(text):
    with open("transactions.txt", "a") as f:
        f.write(text + "\n")


def decision(user):

    if "loan" in user:
        salary = int(input("Enter monthly salary: "))
        if salary >= 30000:
            return "Loan Approved"
        else:
            return "Loan Rejected"

    if "credit card" in user:
        income = int(input("Enter monthly income: "))
        if income >= 25000:
            return "Credit Card Approved"
        else:
            return "Credit Card Rejected"

    if "deposit" in user:
        amt = int(input("Enter amount: "))
        log_transaction("Deposit " + str(amt))
        return "Amount Deposited"

    if "withdraw" in user:
        amt = int(input("Enter amount: "))
        log_transaction("Withdraw " + str(amt))
        return "Amount Withdrawn"

    if "account suggest" in user:
        income = int(input("Enter monthly income: "))
        if income < 25000:
            return "Savings Account Recommended"
        else:
            return "Current Account Recommended"

    return None

greet = ["hi","hello","hey"]
bye = ["bye","exit"]
thanks = ["thanks","thank you"]


def login():
    pin_file = "pin.txt"

    if not os.path.exists(pin_file):
        newpin = input("Create 4 digit PIN: ")
        with open(pin_file,"w") as f:
            f.write(newpin)
        print("PIN created successfully")

    stored = open(pin_file).read().strip()

    for i in range(3):
        pin = input("Enter PIN: ")
        if pin == stored:
            print("Login successful\n")
            return True
        else:
            print("Wrong PIN")

    print("Account locked")
    return False


def bankbot():

    if not login():
        return


    name = get_customer()

    if name == "":
        name = input("Enter your name: ")
        save_customer(name)
    else:
        print("Welcome back", name)

    db = load_db()

    while True:
        user = input(name + ": ").lower()

        if user in bye:
            print("Bot: Thank you for banking with us")
            break

        if user in greet:
            print("Bot: Welcome to Smart Bank,", name)
            continue

        if user in thanks:
            print("Bot: Happy to help!")
            continue

        ans = decision(user)
        if ans:
            print("Bot:", ans)
            continue

        found = False
        for k in db:
            if k in user:
                print("Bot:", db[k])
                found = True
                break

        if not found:
            print("Bot: I don't know. Teach me.")
            new = input("Enter answer: ")
            with open("database.txt", "a") as f:
                f.write("\n" + user + ":" + new)
            print("Bot: Learned new info")

bankbot()

# Write your code here
from random import randint
from math import ceil
import sqlite3

# Connect to database
conn = sqlite3.connect('card.s3db')

# Create a cursor
cur = conn.cursor()
# drop
cur.execute("DROP TABLE card")
conn.commit()

# Create a table
cur.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);""")


def user_signed(current_account):  # User is signed in
    print("You have successfully logged in!")
    while True:
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        choice = int(input())
        print()
        if choice == 1:
            cur.execute("SELECT balance FROM card WHERE number = ?", (current_account,))
            actual_balance = cur.fetchone()
            conn.commit()
            print(f"Balance: {actual_balance}")
            continue
        elif choice == 2:
            print("Enter income:")
            income = int(input())
            cur.execute("UPDATE card SET balance = (balance + ?) WHERE number = (?)", (income, current_account))
            conn.commit()
            print("Income was added!")
            continue
        elif choice == 3:
            print("Enter card number")
            transfer_account = input()
            check_account1 = list(str(transfer_account)[:-2])
            total1 = 0
            total_up1 = 0
            for i in range(len(check_account1)):
                if i % 2 == 0:
                    x = int(check_account1[i]) * 2
                    check_account1[i] = str(x)

            for i in range(len(check_account1)):
                if int(check_account1[i]) > 9:
                    x = int(check_account1[i]) - 9
                    check_account1[i] = str(x)

            for i in range(len(check_account1)):
                total1 += int(check_account1[i])
                total_up1 = int(ceil(total1 / 10)) * 10

            check_sum1 = total_up1 - total1
            if (transfer_account,) in cur.execute('SELECT number FROM card;').fetchall():
                if transfer_account == current_account:
                    print("You can't transfer money to the same account!")
                else:
                    print("Enter how much money you want to transfer:")
                    to_transfer = input()
                    balance_check = cur.execute(
                        f'SELECT balance FROM card WHERE number = {current_account};').fetchone()
                    balance_check = ''.join(map(str, balance_check))
                    if int(to_transfer) > int(balance_check):
                        print("Not enough money!")
                    else:
                        print("Success!")
                        cur.execute(
                            f'UPDATE card SET balance = balance - {to_transfer} WHERE number = {current_account};')
                        cur.execute(
                            f'UPDATE card SET balance = balance + {to_transfer} WHERE number = {transfer_account};')
                        conn.commit()
            if int(transfer_account[-1]) != int(check_sum1):
                print("Probably you made a mistake in the card number. Please try again!")
            else:
                print("Such a card does not exist.")
            continue
        elif choice == 4:
            cur.execute(f"DELETE FROM card WHERE number = {current_account}")
            conn.commit()
            print("The account has been closed!")
            current_account = None
            continue
        elif choice == 5:
            current_account = None
            print("You have successfully logged out!")
            continue
        elif choice == 0:
            current_account = None
            print("Bye!")
            exit()


current_account = None

while True:
    if current_account is None:
        print("1. Create an account\n2. Log into account\n0. Exit")
        action = int(input())
        if action == 1:
            new_acc_no = randint(400000000000000, 400000999999999)
            check_account = list(str(new_acc_no))
            total = 0
            total_up = 0
            for i in range(len(check_account)):
                if i % 2 == 0:
                    x = int(check_account[i]) * 2
                    check_account[i] = str(x)

            for i in range(len(check_account)):
                if int(check_account[i]) > 9:
                    x = int(check_account[i]) - 9
                    check_account[i] = str(x)

            for i in range(len(check_account)):
                total += int(check_account[i])
                total_up = int(ceil(total / 10)) * 10

            check_sum = total_up - total
            new_account = str(new_acc_no) + str(check_sum)

            new_pin = str(randint(1000, 9999))

            cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (new_account, new_pin, 0))
            conn.commit()
            print()
            print(f"Your card has been created\nYour card number:\n{new_account}\nYour card PIN:\n{new_pin}")
        elif action == 2:
            print("Enter your card number:")
            temp_account = input()
            cur.execute("SELECT number FROM card WHERE number = ?", (temp_account,))
            current_account = cur.fetchone()
            print("Enter your PIN:")
            temp_pin = input()
            cur.execute("SELECT pin FROM card WHERE number = ?", (temp_account,))
            pinn = cur.fetchone()
            if temp_account == current_account and temp_pin == pinn:
                user_signed(temp_account)
            else:
                print("Wrong card number or PIN!")
            user_signed(temp_account)
        elif action == 0:
            print("Bye!")
            cur.close()
            conn.close()
            exit()

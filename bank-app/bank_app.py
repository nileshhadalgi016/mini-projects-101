import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    
    # Drop existing tables if they exist
    c.execute("DROP TABLE IF EXISTS accounts")
    c.execute("DROP TABLE IF EXISTS transactions")
    
    # Create tables with all required columns
    c.execute('''CREATE TABLE accounts
                 (account_number TEXT PRIMARY KEY,
                  account_holder TEXT,
                  password TEXT,
                  balance REAL)''')
                  
    c.execute('''CREATE TABLE transactions
                 (account_number TEXT,
                  type TEXT,
                  amount REAL,
                  date TEXT)''')
    
    conn.commit()
    conn.close()

class BankAccount:
    def __init__(self, account_number):
        self.account_number = account_number
        self.balance = 0.0
        self.account_holder = None
        self.load_account()

    def create_table(self):
        # Remove this method as tables are now created during initialization
        pass

    def load_account(self):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('SELECT balance, account_holder FROM accounts WHERE account_number = ?', (self.account_number,))
        result = c.fetchone()
        if result:
            self.balance = result[0]
            self.account_holder = result[1]
        conn.close()

    def get_transactions(self):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('''SELECT type, amount, date FROM transactions 
                    WHERE account_number = ? ORDER BY date DESC LIMIT 10''', 
                 (self.account_number,))
        transactions = c.fetchall()
        conn.close()
        return transactions

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.update_balance()
            self.add_transaction('deposit', amount)
            messagebox.showinfo("Deposit", f"Deposited {amount}. New balance is {self.balance}.")
        else:
            messagebox.showerror("Error", "Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.update_balance()
            self.add_transaction('withdraw', amount)
            messagebox.showinfo("Withdraw", f"Withdrew {amount}. New balance is {self.balance}.")
        else:
            messagebox.showerror("Error", "Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        messagebox.showinfo("Balance", f"Account balance: {self.balance}")

    def update_balance(self):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO accounts (account_number, account_holder, password, balance)
                     VALUES (?, (SELECT account_holder FROM accounts WHERE account_number = ?), 
                             (SELECT password FROM accounts WHERE account_number = ?), ?)''', 
                  (self.account_number, self.account_number, self.account_number, self.balance))
        conn.commit()
        conn.close()

    def add_transaction(self, type, amount):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('''INSERT INTO transactions (account_number, type, amount, date)
                     VALUES (?, ?, ?, datetime('now'))''', (self.account_number, type, amount))
        conn.commit()
        conn.close()

def main():
    # Initialize database before starting the application
    initialize_database()

    def validate_account_creation():
        account_number = account_number_entry.get().strip()
        account_holder = account_holder_entry.get().strip()
        password = password_entry.get()
        
        if not (account_number and account_holder and password):
            messagebox.showerror("Error", "All fields are required!")
            return False
            
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        if c.fetchone():
            conn.close()
            messagebox.showerror("Error", "Account number already exists!")
            return False
        conn.close()
        return True

    def create_account():
        if not validate_account_creation():
            return
            
        account_number = account_number_entry.get().strip()
        account_holder = account_holder_entry.get().strip()
        password = password_entry.get()
        
        try:
            conn = sqlite3.connect('bank.db')
            c = conn.cursor()
            c.execute('''INSERT INTO accounts (account_number, account_holder, password, balance)
                         VALUES (?, ?, ?, 0.0)''', (account_number, account_holder, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            show_login_frame()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")

    def login():
        account_number = login_account_number_entry.get().strip()
        password = login_password_entry.get()
        
        if not (account_number and password):
            messagebox.showerror("Error", "Please enter both account number and password!")
            return
            
        try:
            conn = sqlite3.connect('bank.db')
            c = conn.cursor()
            c.execute('SELECT password FROM accounts WHERE account_number = ?', (account_number,))
            result = c.fetchone()
            conn.close()
            
            if result and result[0] == password:
                global account
                account = BankAccount(account_number)
                show_main_frame()
                update_transaction_history()
            else:
                messagebox.showerror("Error", "Invalid account number or password!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")

    def logout():
        global account
        account = None
        show_login_frame()

    def show_login_frame():
        main_frame.pack_forget()
        create_account_frame.pack_forget()
        login_frame.pack()
        login_account_number_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)

    def show_create_account_frame():
        login_frame.pack_forget()
        main_frame.pack_forget()
        create_account_frame.pack()

    def show_main_frame():
        login_frame.pack_forget()
        create_account_frame.pack_forget()
        main_frame.pack()
        welcome_label.config(text=f"Welcome, {account.account_holder}")
        amount_entry.delete(0, tk.END)

    def update_transaction_history():
        for item in transaction_tree.get_children():
            transaction_tree.delete(item)
        transactions = account.get_transactions()
        for trans in transactions:
            transaction_tree.insert('', 'end', values=trans)

    def perform_transaction(transaction_type):
        try:
            amount = float(amount_entry.get())
            if transaction_type == 'deposit':
                account.deposit(amount)
            else:
                account.withdraw(amount)
            amount_entry.delete(0, tk.END)
            update_transaction_history()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")

    # Create main window
    root = tk.Tk()
    root.title("Bank App")
    root.geometry("400x600")

    # Style configuration
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 10))
    style.configure("TButton", padding=5)

    # Create frames
    login_frame = ttk.Frame(root, padding="10")
    create_account_frame = ttk.Frame(root, padding="10")
    main_frame = ttk.Frame(root, padding="10")

    # Login Frame
    ttk.Label(login_frame, text="Account Number:").grid(row=0, column=0, pady=5)
    login_account_number_entry = ttk.Entry(login_frame)
    login_account_number_entry.grid(row=0, column=1, pady=5)
    
    ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5)
    login_password_entry = ttk.Entry(login_frame, show='*')
    login_password_entry.grid(row=1, column=1, pady=5)
    
    ttk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Button(login_frame, text="Create New Account", command=show_create_account_frame).grid(row=3, column=0, columnspan=2)

    # Create Account Frame
    ttk.Label(create_account_frame, text="Account Number:").grid(row=0, column=0, pady=5)
    account_number_entry = ttk.Entry(create_account_frame)
    account_number_entry.grid(row=0, column=1, pady=5)
    
    ttk.Label(create_account_frame, text="Account Holder:").grid(row=1, column=0, pady=5)
    account_holder_entry = ttk.Entry(create_account_frame)
    account_holder_entry.grid(row=1, column=1, pady=5)
    
    ttk.Label(create_account_frame, text="Password:").grid(row=2, column=0, pady=5)
    password_entry = ttk.Entry(create_account_frame, show='*')
    password_entry.grid(row=2, column=1, pady=5)
    
    ttk.Button(create_account_frame, text="Create Account", command=create_account).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(create_account_frame, text="Back to Login", command=show_login_frame).grid(row=4, column=0, columnspan=2)

    # Main Frame
    welcome_label = ttk.Label(main_frame, text="Welcome")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=10)
    
    ttk.Label(main_frame, text="Amount:").grid(row=1, column=0, pady=5)
    amount_entry = ttk.Entry(main_frame)
    amount_entry.grid(row=1, column=1, pady=5)
    
    ttk.Button(main_frame, text="Deposit", command=lambda: perform_transaction('deposit')).grid(row=2, column=0, pady=5)
    ttk.Button(main_frame, text="Withdraw", command=lambda: perform_transaction('withdraw')).grid(row=2, column=1, pady=5)
    ttk.Button(main_frame, text="Check Balance", command=lambda: account.check_balance()).grid(row=3, column=0, columnspan=2, pady=5)
    
    # Transaction History
    ttk.Label(main_frame, text="Recent Transactions:").grid(row=4, column=0, columnspan=2, pady=5)
    transaction_tree = ttk.Treeview(main_frame, columns=('Type', 'Amount', 'Date'), show='headings', height=5)
    transaction_tree.heading('Type', text='Type')
    transaction_tree.heading('Amount', text='Amount')
    transaction_tree.heading('Date', text='Date')
    transaction_tree.grid(row=5, column=0, columnspan=2, pady=5)
    
    ttk.Button(main_frame, text="Logout", command=logout).grid(row=6, column=0, columnspan=2, pady=10)

    # Start with login frame
    show_login_frame()
    
    root.mainloop()

if __name__ == "__main__":
    main()

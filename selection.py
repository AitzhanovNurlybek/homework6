import psycopg2
import tkinter as tk
from tkinter import messagebox

config = psycopg2.connect(
    host='localhost',
    database='phonebook',
    user='postgres',
    password='1236'
)

def submit():
    username = entry_username.get()
    password = entry_password.get()

    messagebox.showinfo("Login Info", f"Username: {username}\nPassword: {password}")

root = tk.Tk()
root.title("Login")
root.geometry("300x150")

label_username = tk.Label(root, text="Username:")
label_username.pack(pady=6)
entry_username = tk.Entry(root)
entry_username.pack(pady=6)

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=6)
entry_password = tk.Entry(root, show='*')  # To hide password input
entry_password.pack(pady=6)

button_submit = tk.Button(root, text="Submit", command=submit)
button_submit.pack(pady=10)

root.mainloop()

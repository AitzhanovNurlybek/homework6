import psycopg2
import bcrypt
import tkinter as tk
from tkinter import messagebox


class UserAuth:
    def __init__(self, config):
        self.conn = config
        self.cursor = self.conn.cursor()

    def create_user(self, username, password):
        if self.user_exists(username):
            messagebox.showerror("Error", "Username already exists.")
            return False

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        self.conn.commit()
        messagebox.showinfo("Success", "User created successfully.")
        return True

    def user_exists(self, username):

        self.cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        return self.cursor.fetchone() is not None

    def login(self, username, password):

        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = self.cursor.fetchone()

        if result and bcrypt.checkpw(password.encode(), result[0]):
            messagebox.showinfo("Success", "Login successful!")
            return True
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            return False

    def change_password(self, username, new_password):
        if not self.user_exists(username):
            messagebox.showerror("Error", "User does not exist.")
            return False

        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))
        self.conn.commit()
        messagebox.showinfo("Success", "Password changed successfully.")
        return True

    def change_username(self, old_username, new_username):
        if not self.user_exists(old_username):
            messagebox.showerror("Error", "Old username does not exist.")
            return False

        if self.user_exists(new_username):
            messagebox.showerror("Error", "New username already exists.")
            return False

        self.cursor.execute("UPDATE users SET username = %s WHERE username = %s", (new_username, old_username))
        self.conn.commit()
        messagebox.showinfo("Success", "Username changed successfully.")
        return True

    def delete_user(self, username):
        if not self.user_exists(username):
            messagebox.showerror("Error", "User does not exist.")
            return False

        self.cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        self.conn.commit()
        messagebox.showinfo("Success", "User deleted successfully.")
        return True



config = psycopg2.connect(
    host = 'localhost',
    database='phonebook',
    user='postgres',
    password='1236'
)


auth = UserAuth(config)


root = tk.Tk()
root.title("User Authentication")
root.geometry("300x250")


def submit_login():
    username = entry_username.get()
    password = entry_password.get()
    auth.login(username, password)


def submit_new_user():
    username = entry_username.get()
    password = entry_password.get()
    auth.create_user(username, password)


def submit_change_password():
    username = entry_username.get()
    new_password = entry_password.get()
    auth.change_password(username, new_password)

def submit_change_username():
    old_username = entry_username.get()
    new_username = entry_new_username.get()
    auth.change_username(old_username, new_username)


def submit_delete_user():
    username = entry_username.get()
    auth.delete_user(username)


label_username = tk.Label(root, text="Username:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)


button_login = tk.Button(root, text="Login", command=submit_login)
button_login.pack(pady=5)

button_new_user = tk.Button(root, text="New User", command=submit_new_user)
button_new_user.pack(pady=5)

button_change_password = tk.Button(root, text="Change Password", command=submit_change_password)
button_change_password.pack(pady=5)


label_new_username = tk.Label(root, text="New Username:")
label_new_username.pack(pady=5)
entry_new_username = tk.Entry(root)
entry_new_username.pack(pady=5)

button_change_username = tk.Button(root, text="Change Username", command=submit_change_username)
button_change_username.pack(pady=5)

button_delete_user = tk.Button(root, text="Delete User", command=submit_delete_user)
button_delete_user.pack(pady=5)

root.mainloop()

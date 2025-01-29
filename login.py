from tkinter import *
from tkinter import messagebox
import os
import mysql.connector
from mysql.connector import connection

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("400x350+500+200")  # Increased height for register button
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Variables
        self.username = StringVar()
        self.password = StringVar()
        self.reg_username = StringVar()
        self.reg_password = StringVar()
        self.reg_email = StringVar()

        # Main Frame
        login_frame = Frame(self.root, bg='#f0f0f0')
        login_frame.place(x=50, y=50, width=300, height=250)  # Increased height

        # Title
        title = Label(login_frame, text="Login System", font=("Arial", 20, "bold"), 
                     bg='#f0f0f0', fg='#333333')
        title.place(x=80, y=10)

        # Username
        username_label = Label(login_frame, text="Username:", font=("Arial", 12),
                             bg='#f0f0f0', fg='#333333')
        username_label.place(x=30, y=60)
        
        username_entry = Entry(login_frame, textvariable=self.username, 
                             font=("Arial", 12), bd=2, relief=GROOVE)
        username_entry.place(x=120, y=60, width=150)

        # Password
        password_label = Label(login_frame, text="Password:", font=("Arial", 12),
                             bg='#f0f0f0', fg='#333333')
        password_label.place(x=30, y=100)
        
        password_entry = Entry(login_frame, textvariable=self.password, 
                             font=("Arial", 12), bd=2, relief=GROOVE, show="*")
        password_entry.place(x=120, y=100, width=150)

        # Login Button
        login_button = Button(login_frame, text="Login", command=self.login_verify,
                            font=("Arial", 12, "bold"), bg='#4CAF50', fg='white',
                            activebackground='#45a049', cursor='hand2',
                            width=20)
        login_button.place(x=50, y=150)

        # Register Button
        register_button = Button(login_frame, text="Register New User", 
                               command=self.show_register_window,
                               font=("Arial", 12, "bold"), bg='#2196F3', fg='white',
                               activebackground='#1976D2', cursor='hand2',
                               width=20)
        register_button.place(x=50, y=200)

    def show_register_window(self):
        self.register_window = Toplevel(self.root)
        self.register_window.title("Register New User")
        self.register_window.geometry("400x400+500+200")  # Increased height for new field
        self.register_window.config(bg='#f0f0f0')
        
        # Add confirm password variable
        self.reg_confirm_password = StringVar()
        
        # Registration Form
        title = Label(self.register_window, text="Register", font=("Arial", 20, "bold"),
                     bg='#f0f0f0', fg='#333333')
        title.place(x=140, y=20)

        # Username
        Label(self.register_window, text="Username:", font=("Arial", 12),
              bg='#f0f0f0', fg='#333333').place(x=50, y=80)
        Entry(self.register_window, textvariable=self.reg_username,
              font=("Arial", 12)).place(x=150, y=80, width=200)

        # Password
        Label(self.register_window, text="Password:", font=("Arial", 12),
              bg='#f0f0f0', fg='#333333').place(x=50, y=120)
        Entry(self.register_window, textvariable=self.reg_password,
              font=("Arial", 12), show="*").place(x=150, y=120, width=200)

        # Confirm Password
        Label(self.register_window, text="Confirm:", font=("Arial", 12),
              bg='#f0f0f0', fg='#333333').place(x=50, y=160)
        Entry(self.register_window, textvariable=self.reg_confirm_password,
              font=("Arial", 12), show="*").place(x=150, y=160, width=200)

        # Email
        Label(self.register_window, text="Email:", font=("Arial", 12),
              bg='#f0f0f0', fg='#333333').place(x=50, y=200)
        Entry(self.register_window, textvariable=self.reg_email,
              font=("Arial", 12)).place(x=150, y=200, width=200)

        # Register Button
        Button(self.register_window, text="Register", command=self.register_user,
               font=("Arial", 12, "bold"), bg='#4CAF50', fg='white',
               width=20).place(x=100, y=260)

    def register_user(self):
        try:
            # Create database and table if they don't exist
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root"
            )
            cursor = conn.cursor()
            
            # Create database if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS mydata")
            cursor.execute("USE mydata")
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS login (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE
                )
            """)
            conn.commit()
            
            # Now proceed with registration
            if (self.reg_username.get() == "" or self.reg_password.get() == "" or 
                self.reg_confirm_password.get() == "" or self.reg_email.get() == ""):
                messagebox.showerror("Error", "All fields are required")
                return
            
            if self.reg_password.get() != self.reg_confirm_password.get():
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Check if username already exists
            cursor.execute("SELECT username FROM login WHERE username = %s", 
                         (self.reg_username.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return
            
            # Check if email already exists
            cursor.execute("SELECT email FROM login WHERE email = %s", 
                         (self.reg_email.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already exists")
                return

            # Insert new user
            insert_query = "INSERT INTO login (username, password, email) VALUES (%s, %s, %s)"
            values = (
                self.reg_username.get(),
                self.reg_password.get(),
                self.reg_email.get()
            )
            
            cursor.execute(insert_query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Registration successful!")
            self.register_window.destroy()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Error", f"Database Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def login_verify(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s",
                         (self.username.get(), self.password.get()))
            user = cursor.fetchone()
            
            if user:
                messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                self.open_pharmacy()
            else:
                messagebox.showerror("Error", "Invalid Username or Password")
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")  # Added print for debugging
            messagebox.showerror("Error", f"Database Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def open_pharmacy(self):
            os.system('python pharmacy.py')

if __name__ == "__main__":
    root = Tk()
    app = LoginForm(root)  # Create instance of LoginForm
    root.mainloop()
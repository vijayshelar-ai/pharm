from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import connection

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System - Login")
        self.root.geometry("400x500+500+100")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Add Login Frame
        login_frame = Frame(self.root, bg='#f0f0f0')
        login_frame.pack(pady=20)

        # Login Variables
        self.login_username = StringVar()
        self.login_password = StringVar()

        # Login Fields
        Label(login_frame, text="ID:", font=("Arial", 12), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10)
        Entry(login_frame, textvariable=self.login_username, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10)

        Label(login_frame, text="Password:", font=("Arial", 12), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10)
        Entry(login_frame, textvariable=self.login_password, show="*", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        Button(login_frame, text="Login", command=self.login_user,
               font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
               width=20).grid(row=2, columnspan=2, pady=20)

        # Register Button
        Button(login_frame, text="Register New User", command=self.show_register_window,
               font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
               width=20).grid(row=3, columnspan=2)

    def login_user(self):
        if self.login_username.get() == "" or self.login_password.get() == "":
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            # Check credentials
            cursor.execute("""SELECT * FROM login 
                            WHERE username = %s AND password = %s""", 
                         (self.login_username.get(), self.login_password.get()))
            
            user = cursor.fetchone()
            
            if user:
                messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                self.open_pharmacy()
            else:
                messagebox.showerror("Error", "Invalid Username or Password!")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def open_pharmacy(self):
        import pharmacy
        root = Tk()
        pharmacy.PharmacyManagementSystem(root)
        root.mainloop()

    def show_register_window(self):
        self.register_window = Toplevel(self.root)
        self.register_window.title("Register New User")
        self.register_window.geometry("400x400+500+100")
        self.register_window.config(bg='#f0f0f0')
        
        # Registration Variables
        self.reg_username = StringVar()
        self.reg_password = StringVar()
        self.reg_confirm_password = StringVar()
        self.reg_email = StringVar()
        
        # Registration Form
        frame = Frame(self.register_window, bg='#f0f0f0')
        frame.pack(pady=20)
        
        # Add registration fields
        Label(frame, text="ID:", font=("Arial", 12), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10)
        Entry(frame, textvariable=self.reg_username, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10)
        
        Label(frame, text="Password:", font=("Arial", 12), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10)
        Entry(frame, textvariable=self.reg_password, show="*", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=10)
        
        Label(frame, text="Confirm Password:", font=("Arial", 12), bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=10)
        Entry(frame, textvariable=self.reg_confirm_password, show="*", font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=10)
        
        Label(frame, text="Email:", font=("Arial", 12), bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=10)
        Entry(frame, textvariable=self.reg_email, font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=10)
        
        Button(self.register_window, text="Register", command=self.register_user,
               font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
               width=20).pack(pady=20)

    def register_user(self):
        if (self.reg_username.get() == "" or self.reg_password.get() == "" or 
            self.reg_confirm_password.get() == "" or self.reg_email.get() == ""):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if self.reg_password.get() != self.reg_confirm_password.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        try:
            # Database connection
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

           

            # Check if username exists
            cursor.execute("SELECT * FROM login WHERE username = %s", (self.reg_username.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists!")
                return

            # Check if email exists
            cursor.execute("SELECT * FROM login WHERE email = %s", (self.reg_email.get(),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already exists!")
                return

            # Insert new user
            cursor.execute("""INSERT INTO login (username, password, email) 
                            VALUES (%s, %s, %s)""", 
                         (self.reg_username.get(), self.reg_password.get(), self.reg_email.get()))
            
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            
            # Clear fields
            self.reg_username.set("")
            self.reg_password.set("")
            self.reg_confirm_password.set("")
            self.reg_email.set("")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()

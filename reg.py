from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import connection
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System - Login")
        self.root.geometry("400x500+500+100")
        self.root.configure(bg='#f3f3f3')
        self.root.resizable(False, False)

        # Add Login Frame
        login_frame = Frame(self.root, bg='#f3f3f3', bd=10)
        login_frame.pack(pady=40)

        # Login Variables
        self.login_username = StringVar()
        self.login_password = StringVar()
        
        # OTP Variables
        self.otp = StringVar()
        self.generated_otp = ""

        # Login Fields with styling
        Label(login_frame, text="ID:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").grid(row=0, column=0, padx=20, pady=10)
        Entry(login_frame, textvariable=self.login_username, font=("Helvetica", 12), bd=2, relief="solid", width=20).grid(row=0, column=1, padx=20, pady=10)

        Label(login_frame, text="Password:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").grid(row=1, column=0, padx=20, pady=10)
        Entry(login_frame, textvariable=self.login_password, show="*", font=("Helvetica", 12), bd=2, relief="solid", width=20).grid(row=1, column=1, padx=20, pady=10)

        # Login Button with custom style
        Button(login_frame, text="Login", command=self.login_user, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", width=20, height=2).grid(row=2, columnspan=2, pady=20)

        # Register Button with custom style
        Button(login_frame, text="Register New User", command=self.show_register_window, font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", relief="flat", width=20, height=2).grid(row=3, columnspan=2, pady=10)

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))

    def send_otp_email(self, email, otp):
        """Send OTP to user's email"""
        sender_email = "projectbooking665@gmail.com"  # Replace with your email
        sender_password = "xdfs qnxo jhdn puyw"   # Replace with your app password

        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "Email Verification OTP"

            body = f"Your OTP for registration is: {otp}\nThis OTP will expire in 10 minutes."
            message.attach(MIMEText(body, "plain"))

            # Create SMTP session
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")
            return False

    def verify_otp(self):
        """Verify the OTP entered by user"""
        if self.otp.get() == self.generated_otp:
            self.complete_registration()
            self.otp_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid OTP!")

    def show_otp_window(self):
        """Show OTP verification window"""
        self.otp_window = Toplevel(self.register_window)
        self.otp_window.title("OTP Verification")
        self.otp_window.geometry("300x200+550+200")
        self.otp_window.config(bg='#f3f3f3')

        frame = Frame(self.otp_window, bg='#f3f3f3')
        frame.pack(pady=30)

        Label(frame, text="Enter OTP:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").pack()
        Entry(frame, textvariable=self.otp, font=("Helvetica", 12), bd=2, relief="solid", width=20).pack(pady=10)

        Button(frame, text="Verify OTP", command=self.verify_otp, font=("Helvetica", 12, "bold"), 
               bg="#4CAF50", fg="white", relief="flat", width=15).pack(pady=10)

    def show_register_window(self):
        self.register_window = Toplevel(self.root)
        self.register_window.title("Register New User")
        self.register_window.geometry("400x400+500+100")
        self.register_window.config(bg='#f3f3f3')

        # Registration Variables
        self.reg_username = StringVar()
        self.reg_password = StringVar()
        self.reg_confirm_password = StringVar()
        self.reg_email = StringVar()

        # Registration Form with styling
        frame = Frame(self.register_window, bg='#f3f3f3')
        frame.pack(pady=30)

        # Add registration fields with labels and styling
        Label(frame, text="ID:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").grid(row=0, column=0, padx=20, pady=10)
        Entry(frame, textvariable=self.reg_username, font=("Helvetica", 12), bd=2, relief="solid", width=20).grid(row=0, column=1, padx=20, pady=10)

        Label(frame, text="Password:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").grid(row=1, column=0, padx=20, pady=10)
        Entry(frame, textvariable=self.reg_password, show="*", font=("Helvetica", 12), bd=2, relief="solid", width=20).grid(row=1, column=1, padx=20, pady=10)

        Label(frame, text="Confirm Password:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").grid(row=2, column=0, padx=20, pady=10)
        Entry(frame, textvariable=self.reg_confirm_password, show="*", font=("Helvetica", 12), bd=2, relief="solid", width=20).grid(row=2, column=1, padx=20, pady=10)

        Label(frame, text="Email:", font=("Helvetica", 12, "bold"), bg='#f3f3f3', fg="#333").grid(row=3, column=0, padx=20, pady=10)
        Entry(frame, textvariable=self.reg_email, font=("Helvetica", 12), bd=2, relief="solid", width=20).grid(row=3, column=1, padx=20, pady=10)

        Button(self.register_window, text="Register", command=self.initiate_registration, font=("Helvetica", 12, "bold"), 
               bg="#4CAF50", fg="white", relief="flat", width=20, height=2).pack(pady=20)

    def initiate_registration(self):
        """Start the registration process with email verification"""
        if (self.reg_username.get() == "" or self.reg_password.get() == "" or 
            self.reg_confirm_password.get() == "" or self.reg_email.get() == ""):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if self.reg_password.get() != self.reg_confirm_password.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            # Check if username or email already exists
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM login WHERE username = %s OR email = %s", 
                         (self.reg_username.get(), self.reg_email.get()))
            
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or Email already exists!")
                return

            # Generate and send OTP
            self.generated_otp = self.generate_otp()
            if self.send_otp_email(self.reg_email.get(), self.generated_otp):
                messagebox.showinfo("Success", "OTP has been sent to your email!")
                self.show_otp_window()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def complete_registration(self):
        """Complete the registration process after OTP verification"""
        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO login (username, password, email) 
                            VALUES (%s, %s, %s)""", 
                         (self.reg_username.get(), self.reg_password.get(), self.reg_email.get()))
            
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")

            # Clear fields and close registration window
            self.reg_username.set("")
            self.reg_password.set("")
            self.reg_confirm_password.set("")
            self.reg_email.set("")
            self.register_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

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

            cursor.execute("""SELECT * FROM login 
                            WHERE username = %s AND password = %s""", 
                         (self.login_username.get(), self.login_password.get()))
            
            user = cursor.fetchone()
            
            if user:
                messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                self.open_pharmacy()
            else:
                messagebox.showerror("Error", "Invalid ID or Password!")
                
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

if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()
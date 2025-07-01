from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import connection
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import bcrypt  # Added for password encryption
import re  # Add this for regular expression support

class AnimatedButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = getattr(self, 'on_hover_color', '#2980b9')
        self.config(relief="raised")

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self.config(relief="flat")

class FadeLabel(Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.alpha = 0
        self.fade_in()

    def fade_in(self):
        if self.alpha < 1:
            self.alpha += 0.1
            self.configure(fg=f'#{int(self.alpha*255):02x}{int(self.alpha*255):02x}{int(self.alpha*255):02x}')
            self.after(50, self.fade_in)

class AnimatedEntry(Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_fg = '#333333'
        self.default_bg = 'white'
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        self.config(bg='#f0f0f0')
        self._create_border_line('#2980b9')

    def on_focus_out(self, event):
        self.config(bg=self.default_bg)
        self._create_border_line('#d9d9d9')

    def _create_border_line(self, color):
        line = Canvas(self.master, height=2, bg=color, highlightthickness=0)
        line.place(x=self.winfo_x(), 
                  y=self.winfo_y() + self.winfo_height(), 
                  width=self.winfo_width())
        self.after(2000, line.destroy)

class LoginSystem:
    def __init__(self, root):
        self.is_logged_in = False  # Add login state tracking
        self.root = root
        self._setup_window(root)
        self._init_variables()
        self._create_main_container()
        self._create_logo()
        self._create_login_frame()
        self._create_separator()
        self._create_register_section()

    def _setup_window(self, root):
        self.root.title("Pharmacy Management System")
        self._center_window(800, 600)
        self.root.configure(bg='#f5f6fa')
        self.root.resizable(False, False)

    def _center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def _init_variables(self):
        self.login_username = StringVar()
        self.login_password = StringVar()
        self.otp = StringVar()
        self.generated_otp = ""
        self.forgot_password_email = StringVar()

    def _create_main_container(self):
        self.main_container = Frame(self.root, bg='#f5f6fa')
        self.main_container.place(relx=0.5, rely=0.5, anchor=CENTER)

    def _create_logo(self):
        self.logo_label = FadeLabel(
            self.main_container,
            text="💊 Pharmacy Management",
            font=("Helvetica", 24, "bold"),
            bg='#f5f6fa',
            fg='#2c3e50'
        )
        self.logo_label.pack(pady=20)

    def _create_login_frame(self):
        self.login_frame = Frame(
            self.main_container,
            bg='white',
            highlightthickness=1,
            highlightbackground='#e0e0e0',
            highlightcolor='#e0e0e0'
        )
        self.login_frame.pack(padx=40, pady=20)

        self._create_input_field("Username", self.login_username)
        self._create_input_field("Password", self.login_password, show="●")
        self._create_login_button()
        self._create_forgot_password_link()

    def _create_input_field(self, label_text, variable, show=None):
        Label(
            self.login_frame,
            text=label_text,
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        ).pack(anchor=W, padx=20, pady=(20,5))

        entry = AnimatedEntry(
            self.login_frame,
            textvariable=variable,
            font=("Helvetica", 12),
            bd=0,
            width=30,
            show=show
        )
        entry.pack(padx=20, ipady=8)

    def _create_login_button(self):
        self.login_btn = AnimatedButton(
            self.login_frame,
            text="Login",
            command=self.login_user,
            font=("Helvetica", 12, "bold"),
            bg='#3498db',
            fg='white',
            width=25,
            height=2,
            border=0,
            cursor='hand2'
        )
        self.login_btn.on_hover_color = '#2980b9'
        self.login_btn.pack(pady=30)

    def _create_forgot_password_link(self):
        """Create 'Forgot Password' link"""
        forgot_password_btn = Button(
            self.login_frame,
            text="Forgot Password?",
            command=self.show_forgot_password_window,
            font=("Helvetica", 9),
            bg='white',
            fg='#3498db',
            border=0,
            cursor='hand2',
            activeforeground='#2980b9',
            relief="flat"
        )
        forgot_password_btn.pack(pady=(5, 20))

    def show_forgot_password_window(self):
        """Show forgot password window"""
        self.forgot_password_window = Toplevel(self.root)
        self.forgot_password_window.title("Forgot Password")
        self.forgot_password_window.geometry("400x300+550+200")
        self.forgot_password_window.config(bg='#f5f6fa')
        self.forgot_password_window.resizable(False, False)

        # Main container
        container = Frame(
            self.forgot_password_window,
            bg='white',
            highlightthickness=1,
            highlightbackground='#e0e0e0'
        )
        container.place(relx=0.5, rely=0.5, width=350, height=250, anchor=CENTER)

        # Title
        title_label = FadeLabel(
            container,
            text="Forgot Password",
            font=("Helvetica", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(20, 10))

        # Account Type Selection
        account_frame = Frame(container, bg='white')
        account_frame.pack(pady=10)
        
        self.account_type = StringVar(value="user")
        
        Radiobutton(account_frame, text="User Account", variable=self.account_type, 
                   value="user", bg='white').pack(side=LEFT, padx=10)
        Radiobutton(account_frame, text="Admin Account", variable=self.account_type, 
                   value="admin", bg='white').pack(side=LEFT, padx=10)

        # Email input
        email_label = Label(
            container,
            text="Enter your email:",
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        )
        email_label.pack(pady=(5, 0))

        self.forgot_password_email_entry = AnimatedEntry(
            container,
            textvariable=self.forgot_password_email,
            font=("Helvetica", 12),
            width=30
        )
        self.forgot_password_email_entry.pack(pady=5)

        # Send OTP Button
        send_otp_btn = AnimatedButton(
            container,
            text="Send OTP",
            command=self.send_otp_for_password_reset,
            font=("Helvetica", 12, "bold"),
            bg='#2ecc71',
            fg='white',
            width=15,
            height=1,
            border=0,
            cursor='hand2'
        )
        send_otp_btn.on_hover_color = '#27ae60'
        send_otp_btn.pack(pady=20)

    def send_otp_for_password_reset(self):
        """Send OTP to email for password reset"""
        email = self.forgot_password_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter your email!")
            return

        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            # Check if email exists based on account type
            if self.account_type.get() == "admin":
                cursor.execute("SELECT * FROM admin_login WHERE email = %s", (email,))
            else:
                cursor.execute("SELECT * FROM login WHERE email = %s", (email,))

            if not cursor.fetchone():
                messagebox.showerror("Error", "Email not found!")
                return

            # Generate OTP
            self.generated_otp = ''.join(random.choices(string.digits, k=6))
            if self.send_otp_email(email, self.generated_otp):
                messagebox.showinfo("Success", "OTP has been sent to your email!")
                self.show_otp_window_for_password_reset()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def show_otp_window_for_password_reset(self):
        """Show OTP verification window for password reset"""
        self.otp_window = Toplevel(self.forgot_password_window)
        self.otp_window.title("Verify OTP")
        self.otp_window.geometry("400x300+550+200")
        self.otp_window.config(bg='#f5f6fa')
        self.otp_window.resizable(False, False)

        # Main container
        container = Frame(
            self.otp_window,
            bg='white',
            highlightthickness=1,
            highlightbackground='#e0e0e0'
        )
        container.place(relx=0.5, rely=0.5, width=350, height=250, anchor=CENTER)

        # Title
        title_label = FadeLabel(
            container,
            text="OTP Verification",
            font=("Helvetica", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(30, 10))

        # Email display
        email_label = Label(
            container,
            text=f"OTP sent to: {self.forgot_password_email.get()}",
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        )
        email_label.pack(pady=5)

        # OTP Entry
        otp_frame = Frame(container, bg='white')
        otp_frame.pack(pady=20)

        self.otp_entry = AnimatedEntry(
            otp_frame,
            textvariable=self.otp,
            font=("Helvetica", 24),
            width=6,
            justify='center'
        )
        self.otp_entry.pack()
        self.otp_entry.focus()

        # Verify Button
        verify_btn = AnimatedButton(
            container,
            text="Verify OTP",
            command=self.verify_otp_for_password_reset,
            font=("Helvetica", 12, "bold"),
            bg='#2ecc71',
            fg='white',
            width=15,
            height=1,
            border=0,
            cursor='hand2'
        )
        verify_btn.on_hover_color = '#27ae60'
        verify_btn.pack(pady=20)

        # Resend OTP option
        resend_frame = Frame(container, bg='white')
        resend_frame.pack(pady=5)

        Label(
            resend_frame,
            text="Didn't receive the code?",
            font=("Helvetica", 9),
            bg='white',
            fg='#7f8c8d'
        ).pack(side=LEFT, padx=2)

        resend_btn = Label(
            resend_frame,
            text="Resend OTP",
            font=("Helvetica", 9, "bold"),
            bg='white',
            fg='#3498db',
            cursor='hand2'
        )
        resend_btn.pack(side=LEFT)
        resend_btn.bind('<Button-1>', lambda e: self.resend_otp_for_password_reset())

    def resend_otp_for_password_reset(self):
        """Resend OTP for password reset"""
        email = self.forgot_password_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter your email!")
            return

        self.generated_otp = ''.join(random.choices(string.digits, k=6))
        if self.send_otp_email(email, self.generated_otp):
            messagebox.showinfo("Success", "New OTP has been sent!")
            self.otp.set("")  # Clear OTP field
            self.otp_entry.focus()

    def verify_otp_for_password_reset(self):
        """Verify OTP and show new password window"""
        entered_otp = self.otp.get().strip()
        if not entered_otp:
            messagebox.showerror("Error", "Please enter OTP")
            return

        if entered_otp == self.generated_otp:
            self.show_new_password_window()
        else:
            messagebox.showerror("Error", "Invalid OTP!")
            self.otp.set("")  # Clear OTP field
            self.otp_entry.focus()

    def show_new_password_window(self):
        """Show window to enter new password"""
        self.new_password_window = Toplevel(self.otp_window)
        self.new_password_window.title("Reset Password")
        self.new_password_window.geometry("400x300+550+200")
        self.new_password_window.config(bg='#f5f6fa')
        self.new_password_window.resizable(False, False)

        # Main container
        container = Frame(
            self.new_password_window,
            bg='white',
            highlightthickness=1,
            highlightbackground='#e0e0e0'
        )
        container.place(relx=0.5, rely=0.5, width=350, height=250, anchor=CENTER)

        # Title
        title_label = FadeLabel(
            container,
            text="Reset Password",
            font=("Helvetica", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(30, 10))

        # New Password Input
        new_password_label = Label(
            container,
            text="New Password:",
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        )
        new_password_label.pack(pady=(5, 0))

        self.new_password = StringVar()
        self.new_password_entry = AnimatedEntry(
            container,
            textvariable=self.new_password,
            font=("Helvetica", 12),
            width=30,
            show="●"
        )
        self.new_password_entry.pack(pady=5)

        # Confirm New Password Input
        confirm_new_password_label = Label(
            container,
            text="Confirm New Password:",
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        )
        confirm_new_password_label.pack(pady=(5, 0))

        self.confirm_new_password = StringVar()
        self.confirm_new_password_entry = AnimatedEntry(
            container,
            textvariable=self.confirm_new_password,
            font=("Helvetica", 12),
            width=30,
            show="●"
        )
        self.confirm_new_password_entry.pack(pady=5)

        # Update Password Button
        update_password_btn = AnimatedButton(
            container,
            text="Update Password",
            command=self.update_password,
            font=("Helvetica", 12, "bold"),
            bg='#2ecc71',
            fg='white',
            width=15,
            height=1,
            border=0,
            cursor='hand2'
        )
        update_password_btn.on_hover_color = '#27ae60'
        update_password_btn.pack(pady=20)

    def update_password(self):
        """Update password in database"""
        new_password = self.new_password.get().strip()
        confirm_new_password = self.confirm_new_password.get().strip()

        if not new_password or not confirm_new_password:
            messagebox.showerror("Error", "Please enter both passwords!")
            return

        if new_password != confirm_new_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            # Update password with hashed value based on account type
            if self.account_type.get() == "admin":
                cursor.execute("UPDATE admin_login SET password = %s WHERE email = %s",
                           (hashed_password.decode('utf-8'), self.forgot_password_email.get()))
            else:
                cursor.execute("UPDATE login SET password = %s WHERE email = %s",
                           (hashed_password.decode('utf-8'), self.forgot_password_email.get()))
            
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")

            # Close windows
            self.new_password_window.destroy()
            self.otp_window.destroy()
            self.forgot_password_window.destroy()

            # Clear fields
            self.forgot_password_email.set("")
            self.new_password.set("")
            self.confirm_new_password.set("")
            self.otp.set("")

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

            # Check admin_login table first
            cursor.execute("SELECT password FROM admin_login WHERE username = %s", 
                           (self.login_username.get(),))
            admin_result = cursor.fetchone()

            if admin_result:
                stored_hashed_password = admin_result[0]
                if bcrypt.checkpw(self.login_password.get().encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    self.is_logged_in = True
                    self.current_user = self.login_username.get()
                    self.login_btn.config(text="Logging in...")
                    self.root.update()
                    time.sleep(0.5)
                    messagebox.showinfo("Success", "Admin Login Successful!")
                    self.root.destroy()
                    self.open_admin_dashboard()
                    return
                else:
                    messagebox.showerror("Error", "Invalid Username or Password!")
                    self.login_password.set("")
                    return

            # Check login table if not found in admin_login
            cursor.execute("SELECT password FROM login WHERE username = %s", 
                           (self.login_username.get(),))
            user_result = cursor.fetchone()

            if user_result:
                stored_hashed_password = user_result[0]
                if bcrypt.checkpw(self.login_password.get().encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    self.is_logged_in = True
                    self.current_user = self.login_username.get()
                    self.login_btn.config(text="Logging in...")
                    self.root.update()
                    time.sleep(0.5)
                    messagebox.showinfo("Success", "Login Successful!")
                    self.root.destroy()
                    self.open_pharmacy()
                else:
                    messagebox.showerror("Error", "Invalid Username or Password!")
                    self.login_password.set("")
            else:
                messagebox.showerror("Error", "Invalid Username or Password!")
                self.login_password.set("")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def send_otp_email(self, email, otp):
        """Send OTP email - Placeholder implementation"""
        try:
            sender_email = "projectbooking665@gmail.com"  # Replace with your email
            sender_password = "xdfs qnxo jhdn puyw"      # Replace with your password/app-specific password
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = "Your OTP Code"
            
            body = f"Your OTP code is: {otp}\nValid for 10 minutes."
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            return False

    def open_admin_dashboard(self):
        """Open admin dashboard"""
        import Admin
        root = Tk()
        Admin.AdminDashboard(root)
        root.mainloop()

    def open_pharmacy(self):
        if not self.is_logged_in:
            messagebox.showerror("Access Denied", "Please login first!")
            return
            
        import pharmacy
        root = Tk()
        pharmacy.PharmacyManagementSystem(root, self.current_user)
        root.mainloop()

    def _create_separator(self):
        ttk.Separator(self.main_container, orient='horizontal').pack(fill='x', padx=40, pady=20)

    def _create_register_section(self):
        Label(
            self.main_container, 
            text="Don't have an account?",
            font=("Helvetica", 10), 
            bg='#f5f6fa', 
            fg='#7f8c8d'
        ).pack(pady=(0,10))

        register_btn = AnimatedButton(
            self.main_container,
            text="Create New Account",
            command=self.show_register_window,
            font=("Helvetica", 12),
            bg='#2ecc71',
            fg='white',
            width=20,
            height=1,
            border=0,
            cursor='hand2'
        )
        register_btn.on_hover_color = '#27ae60'
        register_btn.pack()

    def show_register_window(self):
        """Show registration window with animation"""
        self.register_window = Toplevel(self.root)
        self.register_window.title("Create New Account")
        self.register_window.geometry("500x600+1500+50")  # Start off-screen
        self.register_window.config(bg='#f5f6fa')
        self.register_window.resizable(False, False)

        # Variables for registration
        self.reg_username = StringVar()
        self.reg_password = StringVar()
        self.reg_confirm_password = StringVar()
        self.reg_email = StringVar()

        # Main container with shadow effect
        register_frame = Frame(
            self.register_window,
            bg='white',
            highlightthickness=1,
            highlightbackground='#e0e0e0',
            highlightcolor='#e0e0e0'
        )
        register_frame.place(relx=0.5, rely=0.5, width=450, height=500, anchor=CENTER)

        # Title
        FadeLabel(
            register_frame,
            text="Create Account",
            font=("Helvetica", 24, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=(30, 10))

        # Subtitle
        FadeLabel(
            register_frame,
            text="Fill in your details",
            font=("Helvetica", 12),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 0))

        # Registration form
        form_frame = Frame(register_frame, bg='white')
        form_frame.pack(pady=20, padx=40)

        # Input fields
        fields = [
            ("Username", self.reg_username),
            ("Email", self.reg_email),
            ("Password", self.reg_password, "*"),
            ("Confirm Password", self.reg_confirm_password, "*")
        ]

        for i, field in enumerate(fields):
            if len(field) == 3:
                label, var, show = field
                self._create_register_field(form_frame, label, var, i, show=show)
            else:
                label, var = field
                self._create_register_field(form_frame, label, var, i)

        # Register button
        register_btn = AnimatedButton(
            register_frame,
            text="Create Account",
            command=self.initiate_registration,
            font=("Helvetica", 14, "bold"),
            bg='#2ecc71',
            fg='white',
            width=20,
            height=2,
            border=0,
            cursor='hand2'
        )
        register_btn.on_hover_color = '#27ae60'
        register_btn.pack(pady=30)

        # Animate window entry
        for i in range(1500, 500, -20):
            self.register_window.geometry(f"500x600+{i}+50")
            self.register_window.update()
            time.sleep(0.001)

    def _create_register_field(self, parent, label_text, variable, row, show=None):
        """Create registration form field"""
        Label(
            parent,
            text=label_text,
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        ).pack(anchor=W, pady=(15,0))

        entry = AnimatedEntry(
            parent,
            textvariable=variable,
            font=("Helvetica", 12),
            bd=0,
            width=35,
            show=show
        )
        entry.pack(pady=5)

    def validate_username(self, username):
        """
        Validate username:
        - Only letters and numbers allowed
        - Must be at least 3 characters long
        - Must start with a letter
        """
        if not username:
            return False, "Username cannot be empty"
        
        # Check if username starts with a letter
        if not username[0].isalpha():
            return False, "Username must start with a letter"
            
        # Check length
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
            
        # Check for special characters
        if not re.match("^[a-zA-Z][a-zA-Z0-9]*$", username):
            return False, "Username can only contain letters and numbers"
            
        return True, "Valid username"

    def initiate_registration(self):
        """Handle registration process"""
        if not all([
            self.reg_username.get(),
            self.reg_password.get(),
            self.reg_confirm_password.get(),
            self.reg_email.get()
        ]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate username
        is_valid, message = self.validate_username(self.reg_username.get())
        if not is_valid:
            messagebox.showerror("Invalid Username", message)
            return

        if self.reg_password.get() != self.reg_confirm_password.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            # Check existing user
            cursor.execute("SELECT * FROM login WHERE username = %s OR email = %s",
                         (self.reg_username.get(), self.reg_email.get()))
            
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or Email already exists!")
                return

            # Send OTP
            self.generated_otp = ''.join(random.choices(string.digits, k=6))
            if self.send_otp_email(self.reg_email.get(), self.generated_otp):
                messagebox.showinfo("Success", "Verification code sent to your email!")
                self.show_otp_window()
                return True
            else:
                messagebox.showerror("Error", "Failed to send verification code. Please try again.")
                return False

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send verification code: {str(e)}")
            return False
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def show_otp_window(self):
        """Show OTP verification window"""
        self.otp_window = Toplevel(self.register_window)
        self.otp_window.title("Verify Email")
        self.otp_window.geometry("400x300+550+200")
        self.otp_window.config(bg='#f5f6fa')
        self.otp_window.resizable(False, False)

        # Create centered container with proper sizing
        container = Frame(
            self.otp_window, 
            bg='white',
            highlightthickness=1,
            highlightbackground='#e0e0e0'
        )
        container.place(relx=0.5, rely=0.5, width=350, height=250, anchor=CENTER)

        # Title with better spacing
        title_label = FadeLabel(
            container,
            text="Email Verification",
            font=("Helvetica", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(30, 10))

        # Email display
        email_label = Label(
            container,
            text=f"OTP sent to: {self.reg_email.get()}",
            font=("Helvetica", 10),
            bg='white',
            fg='#7f8c8d'
        )
        email_label.pack(pady=5)

        # OTP Entry with better styling
        otp_frame = Frame(container, bg='white')
        otp_frame.pack(pady=20)

        self.otp_entry = AnimatedEntry(
            otp_frame,
            textvariable=self.otp,
            font=("Helvetica", 24),
            width=6,
            justify='center'
        )
        self.otp_entry.pack()
        self.otp_entry.focus()

        # Verify Button
        verify_btn = AnimatedButton(
            container,
            text="Verify OTP",
            command=self.verify_otp,
            font=("Helvetica", 12, "bold"),
            bg='#2ecc71',
            fg='white',
            width=15,
            height=1,
            border=0,
            cursor='hand2'
        )
        verify_btn.on_hover_color = '#27ae60'
        verify_btn.pack(pady=20)

        # Resend OTP option
        resend_frame = Frame(container, bg='white')
        resend_frame.pack(pady=5)
        
        Label(
            resend_frame,
            text="Didn't receive the code?",
            font=("Helvetica", 9),
            bg='white',
            fg='#7f8c8d'
        ).pack(side=LEFT, padx=2)
        
        resend_btn = Label(
            resend_frame,
            text="Resend OTP",
            font=("Helvetica", 9, "bold"),
            bg='white',
            fg='#3498db',
            cursor='hand2'
        )
        resend_btn.pack(side=LEFT)
        resend_btn.bind('<Button-1>', lambda e: self.resend_otp())

    def resend_otp(self):
        """Handle OTP resend"""
        self.generated_otp = ''.join(random.choices(string.digits, k=6))
        if self.send_otp_email(self.reg_email.get(), self.generated_otp):
            messagebox.showinfo("Success", "New OTP has been sent!")
            self.otp.set("")  # Clear OTP field
            self.otp_entry.focus()

    def verify_otp(self):
        """Verify OTP and complete registration"""
        entered_otp = self.otp.get().strip()
        if not entered_otp:
            messagebox.showerror("Error", "Please enter OTP")
            return

        if entered_otp == self.generated_otp:
            try:
                conn = connection.MySQLConnection(
                    host="localhost",
                    user="root",
                    password="root",
                    database="mydata"
                )
                cursor = conn.cursor()

                # Hash the password before storing
                hashed_password = bcrypt.hashpw(self.reg_password.get().encode('utf-8'), bcrypt.gensalt())

                # Insert new user with hashed password
                cursor.execute("""INSERT INTO login (username, password, email) 
                                VALUES (%s, %s, %s)""", 
                             (self.reg_username.get(),
                              hashed_password,
                              self.reg_email.get()))
                
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                
                # Close windows
                self.otp_window.destroy()
                self.register_window.destroy()
                
                # Clear fields
                self.reg_username.set("")
                self.reg_password.set("")
                self.reg_confirm_password.set("")
                self.reg_email.set("")
                self.otp.set("")
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {str(err)}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            messagebox.showerror("Error", "Invalid OTP!")
            self.otp.set("")  # Clear OTP field
            self.otp_entry.focus()

if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()
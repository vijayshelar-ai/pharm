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
            command=self.login_user,  # This is now correctly referenced
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
                self.is_logged_in = True  # Set login state
                self.current_user = user[1]  # Store username
                self.login_btn.config(text="Logging in...")
                self.root.update()
                time.sleep(0.5)
                messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                self.open_pharmacy()
            else:
                messagebox.showerror("Error", "Invalid Username or Password!")
                self.login_password.set("")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def open_pharmacy(self):
        if not self.is_logged_in:
            messagebox.showerror("Access Denied", "Please login first!")
            return
            
        import pharmacy
        root = Tk()
        pharmacy.PharmacyManagementSystem(root, self.current_user)  # Pass username to pharmacy system
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
                messagebox.showinfo("Success", "OTP has been sent to your email!")
                self.show_otp_window()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def send_otp_email(self, email, otp):
        """Send OTP verification email"""
        try:
            # Email configuration
            sender_email = "projectbooking665@gmail.com"  # Replace with your email
            sender_password = "xdfs qnxo jhdn puyw"  # Replace with your app password
            
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "Pharmacy Management System - Email Verification"

            # Email body
            body = f"""
            Hello,

            Your verification code is: {otp}

            This code will expire in 10 minutes.
            If you didn't request this code, please ignore this email.

            Best regards,
            Pharmacy Management System
            """
            message.attach(MIMEText(body, "plain"))

            # Create SMTP session
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            return True

        except Exception as e:
            print(f"Email Error: {str(e)}")
            messagebox.showerror("Error", "Failed to send verification code. Please try again.")
            return False

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

                # Insert new user
                cursor.execute("""INSERT INTO login (username, password, email) 
                                VALUES (%s, %s, %s)""", 
                             (self.reg_username.get(),
                              self.reg_password.get(),
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
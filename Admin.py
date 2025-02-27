from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import connection
import sys
import bcrypt

class AdminDashboard:
    def __init__(self, root):
        print("1. Starting AdminDashboard initialization")
        self.root = root
        try:
            print("2. Setting window title")
            self.root.title("Admin Dashboard")
            
            # Make window full screen
            print("3. Setting full screen geometry")
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_width}x{screen_height}+0+0")
            self.root.state('zoomed')  # Maximizes the window
            
            print("4. Creating main frame")
            main_frame = Frame(self.root, bd=2, relief=RIDGE)
            main_frame.place(x=0, y=0, width=screen_width, height=screen_height)
            
            print("5. Adding title")
            title = Label(main_frame, text="Admin Dashboard - User Management", 
                         font=("times new roman", 20, "bold"), bg="blue", fg="white", pady=10)
            title.pack(side=TOP, fill=X)
            
            print("6. Creating button frame")
            self.button_frame = Frame(main_frame, bd=2, relief=RIDGE)
            self.button_frame.place(x=10, y=40, width=screen_width-20, height=40)

            self.update_btn = Button(self.button_frame, text="Update", 
                                   command=self.update_user,
                                   bg="green", fg="white", width=15)
            self.update_btn.pack(side=LEFT, padx=5)

            self.delete_btn = Button(self.button_frame, text="Delete", 
                                   command=self.delete_user,
                                   bg="red", fg="white", width=15)
            self.delete_btn.pack(side=LEFT, padx=5)

            self.register_btn = Button(self.button_frame, text="Add Admin", 
                                     command=self.show_register_window,
                                     bg="blue", fg="white", width=15)
            self.register_btn.pack(side=LEFT, padx=5)

            self.admin_manage_btn = Button(self.button_frame, text="Admin Dashboard", 
                                         command=self.open_admin_management,
                                         bg="purple", fg="white", width=15)
            self.admin_manage_btn.pack(side=LEFT, padx=5)

            print("7. Creating table frame")
            table_frame = Frame(main_frame, bd=2, relief=RIDGE)
            table_frame.place(x=10, y=90, width=screen_width-20, height=screen_height-100)
            
            print("8. Setting up scrollbars")
            scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
            scroll_y = Scrollbar(table_frame, orient=VERTICAL)
            
            print("9. Creating Treeview")
            self.user_table = ttk.Treeview(table_frame,
                                         columns=("id", "password", "confirm_password", "email", "username"),
                                         xscrollcommand=scroll_x.set,
                                         yscrollcommand=scroll_y.set)
            
            print("10. Configuring scrollbars")
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=self.user_table.xview)
            scroll_y.config(command=self.user_table.yview)
            
            print("11. Setting table headings")
            self.user_table.heading("id", text="ID")
            self.user_table.heading("password", text="Password")
            self.user_table.heading("confirm_password", text="Confirm Password")
            self.user_table.heading("email", text="Email")
            self.user_table.heading("username", text="Username")
            self.user_table["show"] = "headings"
            
            print("12. Setting column widths")
            self.user_table.column("id", width=int(screen_width*0.05))
            self.user_table.column("password", width=int(screen_width*0.25))
            self.user_table.column("confirm_password", width=int(screen_width*0.25))
            self.user_table.column("email", width=int(screen_width*0.25))
            self.user_table.column("username", width=int(screen_width*0.15))
            
            print("13. Packing table")
            self.user_table.pack(fill=BOTH, expand=1)
            
            self.reg_username = StringVar()
            self.reg_password = StringVar()
            self.reg_email = StringVar()

            self.user_table.bind('<<TreeviewSelect>>', self.on_tree_select)
            self.selected_item = None

            print("14. Loading data")
            self.fetch_data()
            
        except Exception as e:
            print(f"15. Error in __init__: {str(e)}")
            raise
        
    def fetch_data(self):
        print("16. Entering fetch_data")
        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()
            
            cursor.execute("SHOW TABLES LIKE 'login'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                print("17. Table 'login' not found")
                messagebox.showerror("Error", "Table 'login' does not exist!")
                conn.close()
                return
                
            cursor.execute("SELECT ID, password, confirm_password, email, username FROM login")
            rows = cursor.fetchall()
            
            if rows:
                self.user_table.delete(*self.user_table.get_children())
                for row in rows:
                    self.user_table.insert("", END, values=row)
                conn.commit()
            else:
                messagebox.showinfo("Info", "No records found in login table")
                
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Connection failed: {str(err)}")
            if 'conn' in locals():
                conn.close()

    def on_tree_select(self, event):
        selected_items = self.user_table.selection()
        if selected_items:
            self.selected_item = selected_items[0]
        else:
            self.selected_item = None

    def update_user(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select a user to update")
            return

        self.update_window = Toplevel(self.root)
        self.update_window.title("Update User")
        self.update_window.geometry("400x300")
        self.update_window.resizable(False, False)

        current_values = self.user_table.item(self.selected_item)['values']

        Label(self.update_window, text="Update User Information", 
              font=("times new roman", 15, "bold")).pack(pady=10)

        Label(self.update_window, text="Username:").pack()
        username_var = StringVar(value=current_values[4])
        Entry(self.update_window, textvariable=username_var).pack()

        Label(self.update_window, text="Email:").pack()
        email_var = StringVar(value=current_values[3])
        Entry(self.update_window, textvariable=email_var).pack()

        Label(self.update_window, text="New Password (leave blank to keep current):").pack()
        password_var = StringVar()
        Entry(self.update_window, textvariable=password_var, show="*").pack()

        def save_changes():
            try:
                conn = connection.MySQLConnection(
                    host="localhost",
                    user="root",
                    password="root",
                    database="mydata"
                )
                cursor = conn.cursor()

                if password_var.get().strip():
                    hashed_password = bcrypt.hashpw(
                        password_var.get().encode('utf-8'), 
                        bcrypt.gensalt()
                    ).decode('utf-8')
                    cursor.execute("""
                        UPDATE login 
                        SET username=%s, email=%s, password=%s 
                        WHERE id=%s
                    """, (username_var.get(), email_var.get(), 
                          hashed_password, current_values[0]))
                else:
                    cursor.execute("""
                        UPDATE login 
                        SET username=%s, email=%s 
                        WHERE id=%s
                    """, (username_var.get(), email_var.get(), 
                          current_values[0]))

                conn.commit()
                messagebox.showinfo("Success", "User updated successfully!")
                self.update_window.destroy()  # Only close the update window
                self.fetch_data()  # Refresh data without closing main window

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update user: {err}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()

        Button(self.update_window, text="Save Changes", 
               command=save_changes,
               bg="green", fg="white").pack(pady=20)

    def delete_user(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select a user to delete")
            return

        if not messagebox.askyesno("Confirm Delete", 
                                 "Are you sure you want to delete this user?"):
            return

        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            user_id = self.user_table.item(self.selected_item)['values'][0]
            cursor.execute("DELETE FROM login WHERE id=%s", (user_id,))
            conn.commit()

            messagebox.showinfo("Success", "User deleted successfully!")
            self.fetch_data()  # Refresh data without closing main window

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete user: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def validate_username(self, username):
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in username):
            return False, "Username must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)"

        return True, "Valid username"

    def show_register_window(self):
        self.register_window = Toplevel(self.root)
        self.register_window.title("Register New Admin")
        self.register_window.geometry("400x400")
        self.register_window.resizable(False, False)

        Label(self.register_window, 
              text="Register New Admin", 
              font=("Helvetica", 16, "bold")).pack(pady=10)

        Label(self.register_window, text="Username:").pack(pady=5)
        username_entry = Entry(self.register_window, 
                              textvariable=self.reg_username,
                              width=30)
        username_entry.pack()

        Label(self.register_window, text="Email:").pack(pady=5)
        Entry(self.register_window, 
              textvariable=self.reg_email,
              width=30).pack()

        Label(self.register_window, text="Password:").pack(pady=5)
        Entry(self.register_window, 
              textvariable=self.reg_password,
              show="*",
              width=30).pack()

        Button(self.register_window, 
               text="Register Admin", 
               command=self.register_admin,
               bg="blue", fg="white").pack(pady=20)

    def register_admin(self):
        if not all([self.reg_username.get(), 
                   self.reg_password.get(), 
                   self.reg_email.get()]):
            messagebox.showerror("Error", "All fields are required!")
            return

        is_valid, message = self.validate_username(self.reg_username.get())
        if not is_valid:
            messagebox.showerror("Invalid Username", message)
            return

        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            cursor.execute("""SELECT * FROM admin_login 
                            WHERE username = %s OR email = %s""", 
                         (self.reg_username.get(), 
                          self.reg_email.get()))
            
            if cursor.fetchone():
                messagebox.showerror("Error", 
                                   "Username or Email already exists!")
                return

            hashed_password = bcrypt.hashpw(
                self.reg_password.get().encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            cursor.execute("""
                INSERT INTO admin_login (username, password, email) 
                VALUES (%s, %s, %s)
            """, (self.reg_username.get(),
                 hashed_password,
                 self.reg_email.get()))
            
            conn.commit()
            messagebox.showinfo("Success", 
                              "New admin registered successfully!")
            
            self.reg_username.set("")
            self.reg_password.set("")
            self.reg_email.set("")
            self.register_window.destroy()  # Only close the register window
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def open_admin_management(self):
        """Open new window for admin management"""
        self.admin_window = Toplevel(self.root)
        self.admin_window.title("Admin Management")
        
        # Make admin management window full screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.admin_window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.admin_window.state('zoomed')

        # Main frame
        main_frame = Frame(self.admin_window, bd=2, relief=RIDGE)
        main_frame.place(x=0, y=0, width=screen_width, height=screen_height)

        # Title
        Label(main_frame, text="Admin Management", 
              font=("times new roman", 20, "bold"), bg="purple", fg="white", pady=10).pack(side=TOP, fill=X)

        # Buttons frame
        btn_frame = Frame(main_frame, bd=2, relief=RIDGE)
        btn_frame.place(x=10, y=50, width=screen_width-20, height=40)

        Button(btn_frame, text="Update Admin", command=self.update_admin,
               bg="green", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Delete Admin", command=self.delete_admin,
               bg="red", fg="white", width=15).pack(side=LEFT, padx=5)
        # Add Close button to return to Admin Dashboard manually
        Button(btn_frame, text="Close", command=self.admin_window.destroy,
               bg="grey", fg="white", width=15).pack(side=LEFT, padx=5)

        # Table frame
        table_frame = Frame(main_frame, bd=2, relief=RIDGE)
        table_frame.place(x=10, y=100, width=screen_width-20, height=screen_height-110)

        # Scrollbars
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        # Treeview for admins
        self.admin_table = ttk.Treeview(table_frame,
                                      columns=("id", "username", "password", "email"),
                                      xscrollcommand=scroll_x.set,
                                      yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.admin_table.xview)
        scroll_y.config(command=self.admin_table.yview)

        # Table headings
        self.admin_table.heading("id", text="ID")
        self.admin_table.heading("username", text="Username")
        self.admin_table.heading("password", text="Password")
        self.admin_table.heading("email", text="Email")
        self.admin_table["show"] = "headings"

        # Column widths adjusted for full screen
        self.admin_table.column("id", width=int(screen_width*0.05))
        self.admin_table.column("username", width=int(screen_width*0.25))
        self.admin_table.column("password", width=int(screen_width*0.35))
        self.admin_table.column("email", width=int(screen_width*0.35))

        self.admin_table.pack(fill=BOTH, expand=1)

        self.admin_table.bind('<<TreeviewSelect>>', self.on_admin_select)
        self.selected_admin = None

        self.fetch_admin_data()

    def fetch_admin_data(self):
        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            cursor.execute("SHOW TABLES LIKE 'admin_login'")
            if not cursor.fetchone():
                messagebox.showerror("Error", "Table 'admin_login' does not exist!")
                conn.close()
                return

            cursor.execute("SELECT id, username, password, email FROM admin_login")
            rows = cursor.fetchall()

            self.admin_table.delete(*self.admin_table.get_children())
            for row in rows:
                self.admin_table.insert("", END, values=row)
            conn.commit()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
            if 'conn' in locals():
                conn.close()

    def on_admin_select(self, event):
        selected_items = self.admin_table.selection()
        if selected_items:
            self.selected_admin = selected_items[0]
        else:
            self.selected_admin = None

    def update_admin(self):
        if not self.selected_admin:
            messagebox.showerror("Error", "Please select an admin to update")
            return

        update_window = Toplevel(self.admin_window)
        update_window.title("Update Admin")
        update_window.geometry("400x300")
        update_window.resizable(False, False)

        current_values = self.admin_table.item(self.selected_admin)['values']

        Label(update_window, text="Update Admin Information", 
              font=("times new roman", 15, "bold")).pack(pady=10)

        Label(update_window, text="Username:").pack()
        username_var = StringVar(value=current_values[1])
        Entry(update_window, textvariable=username_var).pack()

        Label(update_window, text="Email:").pack()
        email_var = StringVar(value=current_values[3])
        Entry(update_window, textvariable=email_var).pack()

        Label(update_window, text="New Password (leave blank to keep current):").pack()
        password_var = StringVar()
        Entry(update_window, textvariable=password_var, show="*").pack()

        def save_admin_changes():
            try:
                conn = connection.MySQLConnection(
                    host="localhost",
                    user="root",
                    password="root",
                    database="mydata"
                )
                cursor = conn.cursor()

                if password_var.get().strip():
                    hashed_password = bcrypt.hashpw(
                        password_var.get().encode('utf-8'), 
                        bcrypt.gensalt()
                    ).decode('utf-8')
                    cursor.execute("""
                        UPDATE admin_login 
                        SET username=%s, email=%s, password=%s 
                        WHERE id=%s
                    """, (username_var.get(), email_var.get(), 
                          hashed_password, current_values[0]))
                else:
                    cursor.execute("""
                        UPDATE admin_login 
                        SET username=%s, email=%s 
                        WHERE id=%s
                    """, (username_var.get(), email_var.get(), 
                          current_values[0]))

                conn.commit()
                messagebox.showinfo("Success", "Admin updated successfully!")
                update_window.destroy()  # Only close the update window
                self.fetch_admin_data()  # Refresh data without closing admin management window

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update admin: {err}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()

        Button(update_window, text="Save Changes", 
               command=save_admin_changes,
               bg="green", fg="white").pack(pady=20)

    def delete_admin(self):
        if not self.selected_admin:
            messagebox.showerror("Error", "Please select an admin to delete")
            return

        if not messagebox.askyesno("Confirm Delete", 
                                 "Are you sure you want to delete this admin?"):
            return

        try:
            conn = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            cursor = conn.cursor()

            admin_id = self.admin_table.item(self.selected_admin)['values'][0]
            cursor.execute("DELETE FROM admin_login WHERE id=%s", (admin_id,))
            conn.commit()

            messagebox.showinfo("Success", "Admin deleted successfully!")
            self.fetch_admin_data()  # Refresh data without closing admin management window

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete admin: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    try:
        print("18. Starting main application")
        root = Tk()
        print("19. Creating AdminDashboard instance")
        obj = AdminDashboard(root)
        print("20. Starting mainloop")
        root.mainloop()
    except Exception as e:
        print(f"21. Main block error: {str(e)}")
        sys.exit(1)
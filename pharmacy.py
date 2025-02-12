from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import connection
import openai
import threading
from datetime import datetime

class PharmacyManagementSystem:
    def __init__(self, root, username=None):
        if username is None:
            messagebox.showerror("Access Denied", "Direct access not allowed. Please login first!")
            root.destroy()
            return
            
        self.root = root
        self.username = username
        self.root.title(f"Pharmacy Management System - Logged in as {username}")
        self.root.geometry("1550x800+0+0")
        
        #==================addmed=====================
        self.refmed_var=StringVar()
        self.addmed_var=StringVar()
        
        #==================main table vairiable=====
        
        self.ref_var = StringVar()
        self.company_var = StringVar()
        self.lot_var = StringVar()
        self.type_var = StringVar()
        self.MedName_var = StringVar()  # Remove the comma that made it a tuple
        self.issue_date_var = StringVar()
        self.exp_date_var = StringVar()
        self.uses_var = StringVar()
        self.side_effects_var = StringVar()
        self.precaution_var = StringVar()
        self.dosage_var = StringVar()
        self.price_var = StringVar()
        self.product_qt_var = StringVar()
        
        lbltitle = Label(self.root, text="Pharmacy Management System", bd=15, relief=RIDGE, bg="green", fg="white", font=("times new roman", 50, "bold"),padx=2,pady=4).pack(side=TOP, fill=X)
        
        IMG1 = Image.open("logos.png")
        img1 = IMG1.resize((70, 70), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
        b1 = Button(self.root, image=self.photoimg1,borderwidth=5).place(x=50, y=15.5)
        
        
        
        #============Data Frame=================
        DataFrame = Frame(self.root, bd=15, relief=RIDGE, bg="white")
        DataFrame.place(x=0, y=110, width=1280, height=390)
        
        DataFrameLeft = LabelFrame(DataFrame, bd=15, relief=RIDGE, fg="darkgreen", font=("times new roman", 12, "bold"), text="MEDICINE INFORMATION")
        DataFrameLeft.place(x=0, y=4, width=700, height=355)
        
        # Remove chatbot button from DataFrameLeft by commenting out or deleting these lines:
        # btnChatBot = Button(DataFrameLeft, text="Ask Question", command=self.show_chatbot, 
        #                   font=("arial", 12, "bold"), bg="blue", fg="white", width=10)
        # btnChatBot.grid(row=4, column=3, pady=5, padx=5)

        DataFrameRight = LabelFrame(DataFrame, bd=15, relief=RIDGE, fg="darkgreen", font=("times new roman", 12, "bold"), text="MEDICINE ADD DEPARTMENT")
        DataFrameRight.place(x=700, y=4, width=545, height=355)
        
        #================= Buttons=================
        ButtonFrame = Frame(self.root, bd=15, relief=RIDGE, bg="white")
        ButtonFrame.place(x=0, y=500, width=1280, height=65) 
        #================MAIN BUTTONS=================
        btnAddData = Button(ButtonFrame,command=self.Add_dat, text="MEDICINE ADD", font=("arial", 12, "bold"),bg="darkgreen", fg="white",)
        btnAddData.grid(row=0, column=0) 
        
        btnUpdateMed = Button(ButtonFrame,command=self.Update, text="UPDATE", font=("arial", 12, "bold"),bg="darkgreen", fg="white",)
        btnUpdateMed.grid(row=0, column=1) 
        
        btnDeleteMed = Button(ButtonFrame,command=self.delete, text="DELETE", font=("arial", 12, "bold"),bg="darkred", fg="white",)
        btnDeleteMed.grid(row=0, column=2) 
        
        btnResetMed = Button(ButtonFrame,command=self.reset, text="RESET", font=("arial", 12, "bold"),bg="black", fg="white",)
        btnResetMed.grid(row=0, column=3) 
        
        btnExitMed = Button(ButtonFrame,command=self.exit, text="LOGOUT", font=("arial", 12, "bold"),bg="darkgreen", fg="white",)
        btnExitMed.grid(row=0, column=4) 
        
        
        #=================search Button=======
        
        lblsearch = Label(ButtonFrame, text="Search By", font=("arial", 17, "bold"), bg="gray" ,fg="white")
        lblsearch.grid(row=0, column=5, sticky=W)
        
        # vairiable
        self.search_var = StringVar()
        search_combo = ttk.Combobox(ButtonFrame, textvariable=self.search_var, font=("arial", 16, "bold"), width=13, state="readonly")
        search_combo["values"] = ("Ref", "MedName", "Lot")  # These must match the keys in column_mapping
        search_combo.grid(row=0, column=6)
        search_combo.current(0)
        
        # varibale
        self.searchtxt_var = StringVar()
        txtsearch = Entry(ButtonFrame,textvariable=self.searchtxt_var, font=("arial", 16, "bold"), bd=3, relief=RIDGE)
        txtsearch.grid(row=0, column=7)
        
        btnSearchMed = Button(ButtonFrame,command=self.search_data, text="SEARCH", font=("arial", 12, "bold"),bg="blue", fg="white")
        btnSearchMed.grid(row=0, column=8) 
        
        btnShowMed = Button(ButtonFrame,command=self.fetchh_data,text="SHOW ALL", font=("arial", 12, "bold"),width=8,bg="red", fg="white")
        btnShowMed.grid(row=0, column=9) 
        
        btnRefresh = Button(ButtonFrame, text="REFRESH", font=("arial", 12, "bold"), bg="blue", fg="white",width=7, command=self.refresh_frames)
        btnRefresh.grid(row=0, column=10)
        
        
        #=================label for Data Frame Left ref option=================
        
        lblrefno = Label(DataFrameLeft, text="Reference No : ", font=("arial", 13, "bold"))
        lblrefno.grid(row=0, column=1, sticky=W, pady=5)
        
        #========================connection of left frame data
        #========through right frame data
        print("Connecting to database...")
        connections = connection.MySQLConnection(
            host="localhost",
            user="root",  
            password="root", 
            database="mydata"

        )
      
        my_cursor = connections.cursor()
        my_cursor.execute("select Ref from pharm")
        row = my_cursor.fetchall()
        connections.close()
       
        # Ensure Ref_combo is defined as an instance variable
        self.Ref_combo = ttk.Combobox(DataFrameLeft,textvariable=self.ref_var, font=("arial", 10, "bold"), width=20, state="readonly")
        self.Ref_combo["values"] = [r[0] for r in row]
        self.Ref_combo.grid(row=0, column=2, pady=5)
        
        #=================company name type==================
        
        lblcompno = Label(DataFrameLeft, text="Company Name : ", font=("arial", 13, "bold"))
        lblcompno.grid(row=1, column=1, sticky=W, pady=5)
        
        entrcomp = Entry(DataFrameLeft,textvariable=self.company_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        entrcomp.grid(row=1, column=2, pady=5)
        
         #=================label for Data Frame Left typen of med option==================
        
        lblmedno = Label(DataFrameLeft, text="Type Of Medicine : ", font=("arial", 13, "bold"))
        lblmedno.grid(row=2, column=1, sticky=W, pady=5)
        
        medop_combo = ttk.Combobox(DataFrameLeft,textvariable=self.type_var,font=("arial", 10, "bold"), width=20, state="readonly")
        medop_combo["values"] = ("Tablet", "Liquid", "Capsule","Drops","Injection","Inhaler","Cream") 
        medop_combo.grid(row=2, column=2, pady=5)
        medop_combo.current(0)
         
         #=================label for Data Frame Left typen of med name==================
        
        lblmedname = Label(DataFrameLeft, text="Medicine Name : ", font=("arial", 13, "bold"))
        lblmedname.grid(row=3, column=1, sticky=W, pady=5)
        
         #====================connection for medicine ======
        print("Connecting to database...")
        connections = connection.MySQLConnection(
            host="localhost",
            user="root",  # Ensure this is correct
            password="root",  # Ensure this is correct
            database="mydata"  # Ensure this is correct
        )
      
        my_cursor = connections.cursor()
        my_cursor.execute("select MedName from pharm")
        med = my_cursor.fetchall()
        connections.close()
        
        # Ensure mednam_combo is defined as an instance variable
        self.mednam_combo = ttk.Combobox(DataFrameLeft,textvariable=self.MedName_var,font=("arial", 10, "bold"), width=20, state="readonly")
        self.mednam_combo["values"] = med
        self.mednam_combo.grid(row=3, column=2, pady=5)
        self.mednam_combo.current(0)       
        
         #=================LOT NO==================
        
        lblLOTno = Label(DataFrameLeft, text="Lot No : ", font=("arial", 13, "bold"))
        lblLOTno.grid(row=4, column=1, sticky=W, pady=5)
        
        entrcomp = Entry(DataFrameLeft,textvariable=self.lot_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        entrcomp.grid(row=4, column=2, pady=5)
        
        #=================ISSUE DATE==================
        
        lblisudate = Label(DataFrameLeft, text="Issue Date : ", font=("arial", 13, "bold"))
        lblisudate.grid(row=5, column=1, sticky=W, pady=5)
        
        issueDTcomp = Entry(DataFrameLeft,textvariable=self.issue_date_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        issueDTcomp.grid(row=5, column=2, pady=5)
        
         #=================Expiry Date==================
        
        lblexpdate = Label(DataFrameLeft, text="Exp Date : ", font=("arial", 13, "bold"))
        lblexpdate.grid(row=6, column=1, sticky=W, pady=5)
        
        expiryDTcomp = Entry(DataFrameLeft,textvariable=self.exp_date_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        expiryDTcomp.grid(row=6, column=2, pady=5)
        
           #=================Use medi==================
        
        used = Label(DataFrameLeft, text="Uses : ", font=("arial", 13, "bold"))
        used.grid(row=7, column=1, sticky=W, pady=5)
        
        usedcomp = Entry(DataFrameLeft,textvariable=self.uses_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        usedcomp.grid(row=7, column=2, pady=5)
        
          #=================Side Effect==================
        
        sideeffec = Label(DataFrameLeft, text="Side Effect : ", font=("arial", 13, "bold"))
        sideeffec.grid(row=8, column=1, sticky=W, pady=5)
        
        sudecomp = Entry(DataFrameLeft,textvariable=self.side_effects_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        sudecomp.grid(row=8, column=2, pady=5)
        
          #=================Precau==================
        
        precaution = Label(DataFrameLeft, text="Precaution : ", font=("arial", 13, "bold"))
        precaution.grid(row=0, column=3, sticky=W, pady=5)
        
        precaucomp = Entry(DataFrameLeft,textvariable=self.precaution_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        precaucomp.grid(row=0, column=4, pady=5)
        
          #=================Dosage==================
        
        Dosage = Label(DataFrameLeft, text="Dosage : ", font=("arial", 13, "bold"))
        Dosage.grid(row=1, column=3, sticky=W, pady=5)
        
        dosagecomp = Entry(DataFrameLeft,textvariable=self.dosage_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        dosagecomp.grid(row=1, column=4, pady=5)
         
          #=================Tablet price==================
        
        tablet = Label(DataFrameLeft, text="Tablet Price : ", font=("arial", 13, "bold"))
        tablet.grid(row=2, column=3, sticky=W, pady=5)
        
        dosagecompi = Entry(DataFrameLeft,textvariable=self.price_var ,font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        dosagecompi.grid(row=2, column=4, pady=5)
        
           #=================product quantity==================
        
        proqu = Label(DataFrameLeft, text="Product Qt : ", font=("arial", 13, "bold"))
        proqu.grid(row=3, column=3, sticky=W, pady=5)
        
        procomp = Entry(DataFrameLeft,textvariable=self.product_qt_var,font=("arial", 10, "bold"), bd=2, relief=RIDGE ,width=23)
        procomp.grid(row=3, column=4, pady=5)
         
         
          #=================image=================
        try:
            IMG2 = Image.open("med.jfif")
            img3 = IMG2.resize((280,150), Image.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img3)
            lblimg2 = Label(DataFrame, image=self.photoimg2, bd=7, relief=RIDGE)
            lblimg2.place(x=380, y=172)
        except FileNotFoundError:
            print("Image file 'med.jfif' not found.")
        
        #==============Right Data Frame Image==================
        
        IMG3 = Image.open("dep.jpg")
        img4 = IMG3.resize((500,100), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img4)
        lblimg3 = Label(DataFrame, image=self.photoimg3, bd=7, relief=RIDGE)
        lblimg3.place(x=715, y=25)
        
        #===================reference no entry dataframe left=================
        lblrefno = Label(DataFrameRight, text="Reference No : ", font=("arial", 13, "bold"))
        lblrefno.place(x=80, y=120)
        textrefno = Entry(DataFrameRight,textvariable=self.refmed_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE, width=23)
        textrefno.place(x=200, y=120)
        
        lblmedname = Label(DataFrameRight, text="Medicine Name : ", font=("arial", 13, "bold"))
        lblmedname.place(x=70, y=150)
        textmednm = Entry(DataFrameRight,textvariable=self.addmed_var, font=("arial", 10, "bold"), bd=2, relief=RIDGE, width=23)
        textmednm.place(x=200, y=150)
        
        #===================side frame of data frane rigth side=================
        side_frame=Frame(DataFrameRight, bd=2, relief=RIDGE, bg="white")
        side_frame.place(x=2, y=180, width=400, height=137)
        
        #=============scrollbar=================
        sc_x=ttk.Scrollbar(side_frame, orient=HORIZONTAL)
        sc_x.pack(side=BOTTOM, fill=X)
        sc_y=ttk.Scrollbar(side_frame, orient=VERTICAL)
        sc_y.pack(side=RIGHT, fill=Y)
        
        self.medicine_table = ttk.Treeview(side_frame, column=("ref", "medname"), xscrollcommand=sc_x.set, yscrollcommand=sc_y.set)
        
        sc_x.config(command=self.medicine_table.xview)
        sc_y.config(command=self.medicine_table.yview)
        
        self.medicine_table.heading("ref", text="Reference No")  
        self.medicine_table.heading("medname", text="Medicine Name")
        
        self.medicine_table["show"] = "headings"
        self.medicine_table.column("ref", width=100)
        self.medicine_table.column("medname", width=100)
        self.medicine_table.pack(fill=BOTH, expand=1)
        
        self.medicine_table.bind("<ButtonRelease-1>",self.Medget_cursor)
        
        #===========medicine add buttons====
        
        down_frame = Frame(DataFrameRight, bd=2, relief=RIDGE, bg="white")
        down_frame.place(x=400, y=120, width=120, height=190)  # Changed y from 150 to 120 to move frame up
        
        # Add buttons with reduced padding to fit better
        button_configs = [
            ("ASK AI", "blue", self.show_chatbot),
            ("ADD", "green", self.AddMed),
            ("UPDATE", "purple", self.UpdateMed),
            ("DELETE", "red", self.DeleteMed),
            ("CLEAR", "orange", self.ClearMed)
        ]
        
        for idx, (text, color, command) in enumerate(button_configs):
            btn = Button(down_frame, 
                        text=text,
                        command=command,
                        font=("arial", 11, "bold"),
                        bg=color,
                        fg="white",
                        width=11,
                        pady=2)  # Reduced pady from 4 to 3
            btn.grid(row=idx, column=0, padx=3, pady=1)  # Reduced pady from 3 to 2

        #=========underground frame======
        FRAMEDETAILS=Frame(self.root,bd=8,relief=RIDGE,bg="white")
        FRAMEDETAILS.place(x=0, y=570, width=1275, height=130)
        
        #===========main table & scroll bar=========
        FRAME=Frame(self.root,bd=12,relief=RIDGE,bg="white")
        FRAME.place(x=0,y=570,width=1280,height=130)
        
      
        scroll_x=ttk.Scrollbar(FRAME, orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(FRAME, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        self.PHARM_table=ttk.Treeview(FRAME, column=("REFERENCE", "COMPANYNAME","TYPE","MEDICINENAME","LOTONO","ISSUEDATE","EXPDATE","USES","SIDEEFFECTS","PRECAUTION","DOSAGE","PRICE","PRODUCTQT"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.config(command=self.PHARM_table.xview)
        scroll_y.config(command=self.PHARM_table.yview)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        self.PHARM_table["show"]="headings"
        
        self.PHARM_table.heading("REFERENCE", text="REFERENCE")
        self.PHARM_table.heading("COMPANYNAME", text="COMPANYNAME")
        self.PHARM_table.heading("TYPE", text="TYPE")
        self.PHARM_table.heading("MEDICINENAME", text="MEDICINE NAME")
        self.PHARM_table.heading("LOTONO", text="LOT NO")
        self.PHARM_table.heading("ISSUEDATE", text="ISSUE DATE")
        self.PHARM_table.heading("EXPDATE", text="EXP DATE")
        self.PHARM_table.heading("USES", text="USES")
        self.PHARM_table.heading("SIDEEFFECTS", text="SIDE EFFECTS")
        self.PHARM_table.heading("PRECAUTION", text="PRECAUTION")
        self.PHARM_table.heading("DOSAGE", text="DOSAGE")
        self.PHARM_table.heading("PRICE", text="PRICE")
        self.PHARM_table.heading("PRODUCTQT", text="PRODUCT QT")
        
        self.PHARM_table.pack(fill=BOTH, expand=1)
        
        self.PHARM_table.column("REFERENCE", width=50)
        self.PHARM_table.column("COMPANYNAME", width=59)
        self.PHARM_table.column("TYPE", width=50)
        self.PHARM_table.column("MEDICINENAME", width=59)
        self.PHARM_table.column("LOTONO", width=50)
        self.PHARM_table.column("ISSUEDATE", width=50)
        self.PHARM_table.column("EXPDATE", width=50)
        self.PHARM_table.column("USES", width=45)
        self.PHARM_table.column("SIDEEFFECTS", width=50)
        self.PHARM_table.column("PRECAUTION", width=50)
        self.PHARM_table.column("DOSAGE", width=50)
        self.PHARM_table.column("PRICE", width=50)
        self.PHARM_table.column("PRODUCTQT", width=50)
        self.fetch_dataMed()
        self.fetchh_data()
        self.PHARM_table.bind("<ButtonRelease-1>",self.get_cursor)
        
      #===============================add medicine sql table connection=================
        
    def AddMed(self):
        try:
            print("Connecting to database...")
            connections = connection.MySQLConnection(
                host="localhost",
                user="root",  # Ensure this is correct
                password="root",  # Ensure this is correct
                database="mydata"  # Ensure this is correct
            )
          
            my_cursor = connections.cursor()
            my_cursor.execute("SELECT * FROM pharm WHERE Ref=%s", (self.refmed_var.get(),))
            row = my_cursor.fetchone()
            if row:
                messagebox.showerror("Error", "Reference number already exists. Please use a unique reference number.")
            else:
                my_cursor.execute("INSERT INTO pharm (Ref, MedName) VALUES (%s, %s)", (
                    self.refmed_var.get(),
                    self.addmed_var.get()
                ))
                connections.commit()
                self.fetch_dataMed()
                self.refresh_frames()
                print("Data inserted successfully.")
                messagebox.showinfo("Success", "Medicine Added Successfully")
        except mysql.connector.Error as err:
            print(f"Error: {str(err)}")
            messagebox.showerror("Error", f"Error due to: {str(err)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        if connections and connections.is_connected():
            connections.close()
            print("Database connection closed.")
            
    def fetch_dataMed(self):
        try:
            print("Connecting to database...")
            connections = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            my_cursor = connections.cursor()
            my_cursor.execute("SELECT * FROM pharm")
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.medicine_table.delete(*self.medicine_table.get_children())
                for row in rows:
                    self.medicine_table.insert("", END, values=row)
            connections.commit()
            print("Data fetched successfully.")
        finally:
            if connections.is_connected():
                connections.close()
                print("Database connection closed.")
                
    #===================medgetcursor=================================
            
    def Medget_cursor(self,event=""):
        cursor_row = self.medicine_table.focus()
        content = self.medicine_table.item(cursor_row)
        row = content["values"]
        if row:
            self.refmed_var.set(row[0])
            self.addmed_var.set(row[1])
        
    #=========define update function========
    def UpdateMed(self):
        if self.refmed_var.get() == "" or self.addmed_var.get() == "":
            messagebox.showerror("Error", "All Fields Are Required")
        else:
            connections = connection.MySQLConnection(
                user="root",
                password="root",
                host="localhost",
                database="mydata"
            )
            my_cursor = connections.cursor()
            my_cursor.execute("UPDATE pharm SET MedName=%s WHERE Ref=%s", (
                self.addmed_var.get(),
                self.refmed_var.get()
            ))
            connections.commit()
            self.fetch_dataMed()
            connections.close()
            messagebox.showinfo("Success", "Medicine Has Been Updated")
            
    def DeleteMed(self):
        if self.refmed_var.get() == "" or self.addmed_var.get() == "":
            messagebox.showerror("Error", "Please select a row to delete")
        else:
            try:
                connections = connection.MySQLConnection(
                    user="root",
                    password="root",
                    host="localhost",
                    database="mydata"
                )
                my_cursor = connections.cursor()
                my_cursor.execute("DELETE FROM pharm WHERE Ref=%s", (self.refmed_var.get(),))
                connections.commit()
                self.fetch_dataMed()
                self.refresh_frames()
                messagebox.showinfo("Success", "Medicine Has Been Deleted")
            except mysql.connector.Error as err:
                print(f"Error: {str(err)}")
                messagebox.showerror("Error", f"Error due to: {str(err)}")
            finally:
                if connections.is_connected():
                    connections.close()
                    print("Database connection closed.")
                
    def refresh_frames(self):
        self.fetch_dataMed()
        self.clear_entries()
        self.refresh_medicine_names()
        self.refresh_reference_numbers()

    def clear_entries(self):
        self.refmed_var.set("")
        self.addmed_var.set("")
        # Clear other entries if needed
        # ...existing code...

    def refresh_medicine_names(self):
        try:
            print("Refreshing medicine names...")
            connections = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            my_cursor = connections.cursor()
            my_cursor.execute("SELECT MedName FROM pharm")
            med = my_cursor.fetchall()
            connections.close()
            
            self.mednam_combo["values"] = med
            self.mednam_combo.current(0)
            print("Medicine names refreshed successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {str(err)}")
            messagebox.showerror("Error", f"Error due to: {str(err)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        finally:
            if connections.is_connected():
                connections.close()
                print("Database connection closed.")

    def refresh_reference_numbers(self):
        try:
            print("Refreshing reference numbers...")
            connections = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            my_cursor = connections.cursor()
            my_cursor.execute("SELECT Ref FROM pharm")
            refs = my_cursor.fetchall()
            connections.close()
            
            self.Ref_combo["values"] = [r[0] for r in refs]
            self.Ref_combo.current(0)
            print("Reference numbers refreshed successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {str(err)}")
            messagebox.showerror("Error", f"Error due to: {str(err)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        finally:
            if connections.is_connected():
                connections.close()
                print("Database connection closed.")
                
    def ClearMed(self):
        self.refmed_var.set("")
        self.addmed_var.set("")
                 
 #==================main table==================
 #connection
    def Add_dat(self):
        connections = None
        try:
            # Data validation
            if (self.ref_var.get() == "" or self.company_var.get() == "" or 
                self.type_var.get() == "" or self.MedName_var.get() == ""):
                messagebox.showerror("Error", "Required fields are empty")
                return

            # Database connection
            connections = connection.MySQLConnection(
                host="localhost",
                username="root",
                password="root",
                database="mydata"
            )
            my_cursor = connections.cursor()

            # Check for existing reference
            my_cursor.execute("SELECT * FROM pharmacy WHERE ref=%s", (self.ref_var.get(),))
            if my_cursor.fetchone():
                messagebox.showerror("Error", "Reference number already exists")
                return

            # Insert new record
            sql = """INSERT INTO pharmacy 
                (ref, company_name, type_med, med_name, lot_no, 
                issue_date, exp_date, uses, side_effects, precaution, 
                dosage, price, product_qt) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            values = (
                self.ref_var.get(),
                self.company_var.get(),
                self.type_var.get(),
                self.MedName_var.get(),
                self.lot_var.get(),
                self.issue_date_var.get(),
                self.exp_date_var.get(),
                self.uses_var.get(),
                self.side_effects_var.get(),
                self.precaution_var.get(),
                self.dosage_var.get(),
                self.price_var.get(),
                self.product_qt_var.get()
            )
            
            my_cursor.execute(sql, values)
            connections.commit()
            self.fetchh_data()
            self.fetch_dataMed()
            messagebox.showinfo("Success", "Medicine Added Successfully")
        
        except mysql.connector.Error as err:
            print(f"Error: {str(err)}")
            messagebox.showerror("Error", f"Database Error: {str(err)}")
        finally:
            if connections and connections.is_connected():
                connections.close()
                
    def fetchh_data(self):
        connections = connection.MySQLConnection(host="localhost", user="root", password="root", database="mydata")
        my_cursor = connections.cursor()
        my_cursor.execute("SELECT * FROM pharmacy")
        row=my_cursor.fetchall()
        if len(row) != 0:
            self.PHARM_table.delete(*self.PHARM_table.get_children())
            for i in row:
                self.PHARM_table.insert("", END, values=i)
            connections.commit()
            connections.close()
            
    def get_cursor(self, event=""):
        cursor_row = self.PHARM_table.focus()
        content = self.PHARM_table.item(cursor_row)
        row = content["values"]
        if row:
            self.ref_var.set(row[0])
            self.company_var.set(row[1])
            self.issue_date_var.set(row[5])
            self.exp_date_var.set(row[6])
            self.uses_var.set(row[7])
            self.side_effects_var.set(row[8])
            self.precaution_var.set(row[9])
            self.dosage_var.set(row[10])
            self.price_var.set(row[11])
            self.product_qt_var.set(row[12])
            
    def Update(self):
        connections = connection.MySQLConnection(host="localhost", user="root", password="root", database="mydata")
        my_cursor = connections.cursor()
        my_cursor.execute("UPDATE pharmacy SET company_name=%s, type_med=%s, med_name=%s, lot_no=%s, issue_date=%s, exp_date=%s, uses=%s, side_effects=%s, precaution=%s, dosage=%s, price=%s, product_qt=%s WHERE ref=%s", (
            self.company_var.get(),
            self.type_var.get(),
            self.MedName_var.get(),
            self.lot_var.get(),
            self.issue_date_var.get(),
            self.exp_date_var.get(),
            self.uses_var.get(),
            self.side_effects_var.get(),
            self.precaution_var.get(),
            self.dosage_var.get(),
            self.price_var.get(),
            self.product_qt_var.get(),
            self.ref_var.get()
        ))
        connections.commit()
        self.fetchh_data()
        self.refresh_frames()
        messagebox.showinfo("Success", "Medicine Has Been Updated")
        connections.close()
    
    def delete(self):
        connections = connection.MySQLConnection(host="localhost", user="root", password="root", database="mydata")
        my_cursor = connections.cursor()
        my_cursor.execute("DELETE FROM pharmacy WHERE ref=%s", (self.ref_var.get(),))
        connections.commit()
        self.fetchh_data()
        self.refresh_frames()
        messagebox.showinfo("Success", "Medicine Has Been Deleted")
        connections.close()
            
    def reset(self):
        self.company_var.set(""),
       # self.type_var.set(""),
       # self.MedName_var.set(""),
        self.lot_var.set(""),
        self.issue_date_var.set(""),
        self.exp_date_var.set(""),
        self.uses_var.set(""),
        self.side_effects_var.set(""),
        self.precaution_var.set(""),
        self.dosage_var.set(""),
        self.price_var.set(""),
        self.product_qt_var.set(""),
       # self.ref_var.set("")
       
    def search_data(self):
        if self.search_var.get() == "" or self.searchtxt_var.get() == "":
            messagebox.showerror("Error", "Please select search criteria and enter search value")
            return
            
        try:
            connections = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            my_cursor = connections.cursor()
            
            # Map display names to database column names
            column_mapping = {
                "Ref": "ref",
                "MedName": "med_name",  # Changed from MedName to med_name
                "Lot": "lot_no"         # Changed from Lot to lot_no
            }
            
            search_criteria = self.search_var.get()
            if search_criteria not in column_mapping:
                messagebox.showerror("Error", "Invalid search criteria")
                return
                
            # Get the correct database column name
            db_column = column_mapping[search_criteria]
            search_value = self.searchtxt_var.get()
            
            # Use parameterized query with correct column name
            sql_query = f"SELECT * FROM pharmacy WHERE {db_column} LIKE %s"
            search_pattern = f"%{search_value}%"
            
            my_cursor.execute(sql_query, (search_pattern,))
            rows = my_cursor.fetchall()
            
            if len(rows) != 0:
                self.PHARM_table.delete(*self.PHARM_table.get_children())
                for row in rows:
                    self.PHARM_table.insert("", END, values=row)
                messagebox.showinfo("Success", f"Found {len(rows)} record(s)")
            else:
                messagebox.showinfo("Not Found", "No matching records found")
                self.fetchh_data()  # Reset to show all records
                
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")  # For debugging
            messagebox.showerror("Error", f"Database Error: {str(err)}")
        finally:
            if connections and connections.is_connected():
                connections.close()
                
    def exit(self):
        self.exit = messagebox.askyesno("Pharmacy Management System", "Do you want to logout?")
        if self.exit > 0:
            self.root.destroy()
            # Optionally reopen login window
            from reg import LoginSystem
            root = Tk()
            LoginSystem(root)
            root.mainloop()
        return

    def get_medicine_info(self, search_term):
        try:
            connections = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="root",
                database="mydata"
            )
            my_cursor = connections.cursor(dictionary=True)
            
            # Search across multiple columns
            query = """
            SELECT * FROM pharmacy 
            WHERE med_name LIKE %s 
            OR ref LIKE %s 
            OR company_name LIKE %s
            LIMIT 1
            """
            search_pattern = f"%{search_term}%"
            my_cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            result = my_cursor.fetchone()
            
            connections.close()
            return result
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None

    def process_question(self, question):
        question = question.lower().strip()
        
        # General greetings
        if any(word in question for word in ["hello", "hi", "hey"]):
            return "Hello! How can I help you with your pharmacy queries today?"
        
        # Look for price related questions
        if "price" in question or "cost" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"The price of {med_info['med_name']} is ${med_info['price']}"
            return "Could you please specify which medicine's price you'd like to know?"
        
        # Look for precaution related questions
        if "precaution" in question or "warning" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"Precautions for {med_info['med_name']}: {med_info['precaution']}"
            return "Please specify which medicine's precautions you'd like to know about."
        
        # Look for side effects
        if "side effect" in question or "side-effect" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"Side effects of {med_info['med_name']}: {med_info['side_effects']}"
            return "Which medicine's side effects would you like to know about?"
        
        # Look for dosage information
        if "dose" in question or "dosage" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"Dosage for {med_info['med_name']}: {med_info['dosage']}"
            return "Please specify which medicine's dosage you'd like to know about."
        
        # Look for uses/indications
        if "use" in question or "used for" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"Uses of {med_info['med_name']}: {med_info['uses']}"
            return "Which medicine's uses would you like to know about?"
        
        # Look for expiry date
        if "expiry" in question or "expiration" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"Expiry date of {med_info['med_name']}: {med_info['exp_date']}"
            return "Which medicine's expiry date would you like to know about?"
        
        # Check stock/quantity
        if "stock" in question or "available" in question or "quantity" in question:
            for word in question.split():
                if med_info := self.get_medicine_info(word):
                    return f"Current stock of {med_info['med_name']}: {med_info['product_qt']} units"
            return "Which medicine's stock level would you like to know about?"

        # General medicine information
        for word in question.split():
            if med_info := self.get_medicine_info(word):
                return f"""Information about {med_info['med_name']}:
- Price: ${med_info['price']}
- Dosage: {med_info['dosage']}
- Uses: {med_info['uses']}
- Side Effects: {med_info['side_effects']}
- Precautions: {med_info['precaution']}
- Stock Available: {med_info['product_qt']} units"""
        
        return "I'm not sure about that. You can ask me about medicine prices, dosages, side effects, precautions, or stock availability."

    def show_chatbot(self):
        chat_window = Toplevel(self.root)
        chat_window.title("Smart Pharmacy Assistant")
        chat_window.geometry("600x500")
        
        # Create main frame
        main_frame = Frame(chat_window)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Create chat display with scrollbar
        chat_frame = Frame(main_frame)
        chat_frame.pack(fill=BOTH, expand=True)
        
        chat_display = Text(chat_frame, wrap=WORD, width=60, height=20)
        scrollbar = ttk.Scrollbar(chat_frame, orient=VERTICAL, command=chat_display.yview)
        chat_display.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=RIGHT, fill=Y)
        chat_display.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Create input area
        input_frame = Frame(chat_window)
        input_frame.pack(fill=X, padx=10, pady=5)
        
        user_input = Entry(input_frame, width=50)
        user_input.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        def handle_question():
            question = user_input.get().strip()
            if not question:
                return
            
            # Add user question to chat
            chat_display.configure(state='normal')
            chat_display.insert(END, f"\nYou: {question}\n")
            
            # Get and display response
            response = self.process_question(question)
            chat_display.insert(END, f"Assistant: {response}\n")
            
            chat_display.configure(state='disabled')
            chat_display.see(END)
            user_input.delete(0, END)
        
        # Add buttons
        send_button = Button(input_frame, text="Send", command=handle_question,
                           font=("arial", 10, "bold"), bg="green", fg="white")
        send_button.pack(side=LEFT, padx=5)
        
        def clear_chat():
            chat_display.configure(state='normal')
            chat_display.delete(1.0, END)
            chat_display.insert(END, "Assistant: How can I help you today?\n")
            chat_display.configure(state='disabled')
        
        # Add control buttons
        button_frame = Frame(chat_window)
        button_frame.pack(fill=X, padx=10, pady=5)
        
        clear_button = Button(button_frame, text="Clear Chat", command=clear_chat,
                            font=("arial", 10, "bold"), bg="orange", fg="white")
        clear_button.pack(side=LEFT, padx=5)
        
        close_button = Button(button_frame, text="Close", command=chat_window.destroy,
                            font=("arial", 10, "bold"), bg="red", fg="white")
        close_button.pack(side=LEFT, padx=5)
        
        # Bind Enter key
        user_input.bind('<Return>', lambda event: handle_question())
        
        # Initial greeting
        chat_display.configure(state='normal')
        chat_display.insert(END, """Assistant: Hello! I can help you with:
- Medicine prices
- Dosage information
- Side effects
- Precautions
- Stock availability
- Expiry dates
- General medicine information

What would you like to know?\n""")
        chat_display.configure(state='disabled')
        
        # Focus on input
        user_input.focus()

if __name__ == "__main__":
    # Prevent direct access
    root = Tk()
    messagebox.showerror("Access Denied", "Please login through the login system.")
    root.destroy()

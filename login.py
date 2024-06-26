from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns



def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()

class Login_Window:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Login")
        self.root.geometry("1600x900+0+0")
        self.root.configure(bg="#e9ebee")
        frame = Frame(self.root, bg="#00bfff")
        frame.place(x=550, y=190, width=440, height=450)

        lbl_login=Label(frame,text="Login To Continue",font=("Arial",20,"bold"),fg="#ffffff",bg="#00bfff")
        lbl_login.place(x=0,y=0,width=440, height=50)

        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill='x')

        lbl_username = Label(frame, text="User Name:", font=("arial", 15, "bold"), fg="#ffffff", bg="#00bfff")
        lbl_username.place(x=50, y=175)
        self.txt_username = Entry(frame, font=("arial", 15, "bold"), width=19)
        self.txt_username.place(x=175, y=175)

        lbl_password = Label(frame, text="Password:", font=("arial", 15, "bold"), fg="#ffffff", bg="#00bfff")
        lbl_password.place(x=50, y=250)
        self.txt_password = Entry(frame, font=("arial", 15, "bold"), width=19, show="*")  # Show asterisks for password
        self.txt_password.place(x=175, y=250)

        login_btn = Button(frame, text="Login",command=self.login, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="#ffffff", bg="#0f9d58", activebackground="white", activeforeground="gray" )
        login_btn.place(x=85, y=330, height=50, width=100)

        signup_btn = Button(frame,command=self.registerwindow, text="Sign Up", font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="#ffffff", bg="#0f9d58", activebackground="white", activeforeground="gray")
        signup_btn.place(x=260, y=330, height=50, width=100)

        forgot_pw_btn = Button(frame, text="Forgot password",command=self.forgotpasswordWindow, font=("arial", 10, "bold"), bd=0, relief=RIDGE, fg="#550a35", bg="#00bfff", activebackground="white", activeforeground="gray")
        forgot_pw_btn.place(x=50, y=280)


    def registerwindow(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)


    def forgotpasswordWindow(self):
        self.root.withdraw()   
        self.new_window=Toplevel(self.root)
        self.app=forgotpassword(self.new_window)

    def login(self):
        if self.txt_username.get() == "" or self.txt_password.get() == "":
            messagebox.showerror("Error", "Please Enter username or password")
            self.txt_username.focus()
        else:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(self.txt_username.get(),
                                                                                    self.txt_password.get(),))
            row = my_cursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid username and password")
            else:
                self.root.withdraw()   # hide current window
                new_window = Toplevel()
                app = Main_Menu(new_window)
                    
            conn.commit()
            conn.close() 
        



class Register:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")

        # Variable
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()
        self.var_check = IntVar()

        frame = Frame(self.root, bg="#9e7bff")
        frame.place(x=400, y=100, width=800, height=550)

        fname = Label(frame, text="First Name", font=("arial", 15, "bold"), fg="#ffffff", bg="#9e7bff")
        fname.place(x=150, y=100)
        fname = ttk.Entry(frame, textvariable=self.var_fname, font=("arial", 15, "bold"))
        fname.place(x=340, y=100, width=250)

        lname = Label(frame, text="Last Name", font=("arial", 15, "bold"), fg="#ffffff", bg="#9e7bff")
        lname.place(x=150, y=150)
        lname = ttk.Entry(frame, textvariable=self.var_lname, font=("arial", 15, "bold"))
        lname.place(x=340, y=150, width=250)

        email = Label(frame, text="Email", font=("arial", 15, "bold"), fg="#ffffff", bg="#9e7bff")
        email.place(x=150, y=200)
        email = ttk.Entry(frame, textvariable=self.var_email, font=("arial", 15, "bold"))
        email.place(x=340, y=200, width=250)

        password = Label(frame, text="Password:", font=("arial", 15, "bold"), fg="#ffffff", bg="#9e7bff")
        password.place(x=150, y=250)
        password = Entry(frame, textvariable=self.var_pass, font=("arial", 15, "bold"), width=19, show="*")
        password.place(x=340, y=250, width=250)

        confpassword = Label(frame, text="Confirm Password:", font=("arial", 15, "bold"), fg="#ffffff", bg="#9e7bff")
        confpassword.place(x=150, y=300)
        conf_password = Entry(frame, textvariable=self.var_confpass, font=("arial", 15, "bold"), width=19, show="*")
        conf_password.place(x=340, y=300, width=250)

        # Checkbtn = Checkbutton(frame, text="I Agree the Terms & Conditions", variable=self.var_check, font=("arial", 10, "bold"),fg="#ffffff", background="#9e7bff", onvalue=1, offvalue=0)
        # Checkbtn.place(x=300, y=370)

        register_btn = Button(frame, text="Register", command=self.register_data, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="#98fb98", activebackground="white", activeforeground="gray")
        register_btn.place(x=255, y=450, height=50, width=100)

        login_btn = Button(frame, text="Login", command=self.loginwindow, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="#98fb98", activebackground="white", activeforeground="gray")
        login_btn.place(x=455, y=450, height=50, width=100)

    
        
    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "":
            messagebox.showerror("Error", "Please enter name and email")
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error", "PASSWORD and CONFIRM PASSWORD must be the same")
        # elif self.var_check.get() == 0:
        #     messagebox.showerror("Error", "Please agree to the terms and conditions")
        else:
            conn=mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            val=(self.var_email.get(),)
            my_cursor.execute(query,val)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist try another Email")
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s)",(self.var_fname.get(),self.var_lname.get(),self.var_email.get(),self.var_pass.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success","registeration complete")


    def loginwindow(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Login_Window(self.new_window)



class forgotpassword:
    def __init__(self,root) -> None:
        self.root = root
        self.root.title("Reset Password")
        self.root.geometry("1600x900+0+0")
  

        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()
        

        frame = Frame(self.root, bg="#ffebcd")
        frame.place(x=400, y=100, width=800, height=550)

        reset = Label(frame, text="Reset your Password", font=("arial", 25, "bold"), bg="#ffebcd")
        reset.place(x=225, y=0)
        email = Label(frame, text="Email", font=("arial", 15, "bold"), bg="#ffebcd")
        email.place(x=50, y=200)
        email = ttk.Entry(frame, textvariable=self.var_email, font=("arial", 15, "bold"))
        email.place(x=280, y=200, width=250)

        password = Label(frame, text="New Password:", font=("arial", 15, "bold"), bg="#ffebcd")
        password.place(x=50, y=250)
        password = Entry(frame, textvariable=self.var_pass, font=("arial", 15, "bold"), width=19, show="*")
        password.place(x=280, y=250, width=250)

        confpassword = Label(frame, text="Confirm Password:", font=("arial", 15, "bold"), bg="#ffebcd")
        confpassword.place(x=50, y=300)
        conf_password = Entry(frame, textvariable=self.var_confpass, font=("arial", 15, "bold"), width=19, show="*")
        conf_password.place(x=280, y=300, width=250)

        update_btn = Button(frame, text="Update Password", command=self.update_pass, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="#dcd0ff", activebackground="white", activeforeground="gray")
        update_btn.place(x=170, y=450, height=50, width=180)

        login_back_btn = Button(frame, text="back to Login",command=self.loginwindow, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="#dcd0ff", activebackground="white", activeforeground="gray")
        login_back_btn.place(x=450, y=450, height=50, width=180)

    def update_pass(self):
        if self.var_email.get() == "" or self.var_pass.get() == "":
            messagebox.showerror("Error", "Please Enter email or password")
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error", "PASSWORD and CONFIRM PASSWORD must be the same")
        else:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            
            # Use the correct syntax for the UPDATE statement
            my_cursor.execute("UPDATE register SET password=%s WHERE email=%s", (self.var_pass.get(), self.var_email.get()))
            
            messagebox.showinfo('Success', "Password is updated")
            conn.commit()
            conn.close()
    
    def loginwindow(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Login_Window(self.new_window)



class Main_Menu:
    def __init__(self,root):
        self.root=root
        self.root.title("MENU")
        self.root.geometry("1600x900+0+0")


        frame = Frame(self.root, bg="#f67280")
        frame.place(x=400, y=100, width=800, height=550)
        
        Pharma_btn = Button(frame, text="Pharmacy Management System", command=self.Pharmacy_m_s, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="#52595d", bg="#98fb98", activebackground="white", activeforeground="gray")
        Pharma_btn.place(x=150, y=150, height=50, width=500)

        report_record_btn = Button(frame, text="Report", command=self.sale_report ,font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="#52595d", bg="#98fb98", activebackground="white", activeforeground="gray")
        report_record_btn.place(x=150, y=250, height=50, width=500)

        Billing_system_btn = Button(frame, text="Billing System",command=self.Billing_system , font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="#52595d", bg="#98fb98", activebackground="white", activeforeground="gray")
        Billing_system_btn.place(x=150, y=350, height=50, width=500)

        menu_back_btn = Button(frame, text="Back to Login",command=self.loginwindow , font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="#ffffff", bg="#16e2f5", activebackground="white", activeforeground="gray")
        menu_back_btn.place(x=300, y=450, height=50, width=200)
        

    def loginwindow(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Login_Window(self.new_window)

    def Pharmacy_m_s(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=PharmacyManagementSystem(self.new_window)

    def sale_report(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Report(self.new_window)

    def Billing_system(self):
        self.root.withdraw()
        self.new_window=Toplevel(self.root)
        self.app=Billing(self.new_window)
    


        # def a new method for patient records



class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="#9cd6fb")
        # self.root.iconbitmap('images/logo.ico')
        self.root.title("Pharmacy Management System")
        self.root.geometry("1530x800+0+0")

        lbltitle = tk.Label(self.root, text=" PHARMACY MANAGEMENT SYSTEM ", bd=1, relief=tk.RIDGE, bg='#174487',
                            fg="#FFFFFF", font=("times new roman", 50, "bold"), padx=2, pady=4)
        lbltitle.pack(side=tk.TOP, fill=tk.X)
        

        #search variables

        self.search_var=tk.StringVar()

        #search txt variable

        self.txtsearch_var=tk.StringVar()
        
        #down frame variables
        self.refNoDown_var = tk.StringVar()
        self.medNameDown_var = tk.StringVar()
        




        # AddMed variable

        self.refMed_var = tk.StringVar()
        self.companyName_var = tk.StringVar()
        self.typeMed_var = tk.StringVar()
        self.tabletName_var = tk.StringVar()
        self.LotNo_var = tk.StringVar()
        self.issueDate_var = tk.StringVar()
        self.expDate_var = tk.StringVar()
        self.uses_var = tk.StringVar()
        self.sideEffect_var = tk.StringVar()
        self.pre_warning_var = tk.StringVar()
        self.dosage_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.productQt_var = tk.StringVar()
        # Data frame
        DataFrame = tk.Frame(self.root, bd=0, bg="#9cd6fb",relief=tk.RIDGE, padx=20)
        DataFrame.place(x=0, y=120, width=1530, height=400)

        DataFrameLeft = tk.LabelFrame(DataFrame, bg="#9cd6fb", bd=0, relief=tk.RIDGE, padx=0, text="Medicine Information",
                                      fg="#273736", font=("arial", 25, "bold"),pady=40)
        DataFrameLeft.place(x=0, y=5, width=950, height=350,)

        DataFrameRight = tk.LabelFrame(DataFrame, bg="#9cd6fb", fg="#273736", bd=0, relief=tk.RIDGE, padx=20,
                                       text="Medicine Add Department", font=("arial", 25, "bold"))
        DataFrameRight.place(x=970, y=5, width=500, height=350)

        # Button Frame
        ButtonFrame = tk.Frame(self.root, bd=5, relief=tk.RIDGE,bg="#9cd6fb" ,padx=20)
        ButtonFrame.place(x=0, y=520, width=1530, height=65,)

        # Labels and Entry
        lblrefno = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Reference No",padx=2)
        lblrefno.grid(row=0, column=0, sticky=tk.W)

        ref_combo = tk.Entry(DataFrameLeft,textvariable=self.refMed_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        ref_combo.grid(row=0, column=1)

        lblcmpName = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Company Name", padx=2)
        lblcmpName.grid(row=1, column=0, sticky=tk.W)
        txtcmpName = tk.Entry(DataFrameLeft, textvariable=self.companyName_var , font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtcmpName.grid(row=1, column=1)

        lblTypeofMedicne = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Type of Medicne", padx=2, pady=6)
        lblTypeofMedicne.grid(row=2, column=0, sticky=tk.W)

        comTypeofMedicine = ttk.Combobox(DataFrameLeft,textvariable=self.typeMed_var, width=27, font=("arial", 12, "bold"), state="readonly")
        comTypeofMedicine["values"] = ("Tablet", "liquid", "Capsules", "Topical Medicines", "Drops", "Inhaler",
                                       "Injection")
        comTypeofMedicine.current(0)
        comTypeofMedicine.grid(row=2, column=1)

        lblMedicneName = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Medicine Name :", padx=2, pady=6)
        lblMedicneName.grid(row=3, column=0, sticky=tk.W)

        txtMedicineName = tk.Entry(DataFrameLeft,textvariable=self.tabletName_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtMedicineName.grid(row=3, column=1)

        lblLotNo = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Lot No. :", padx=2)
        lblLotNo.grid(row=4, column=0, sticky=tk.W)
        txtLotNo = tk.Entry(DataFrameLeft,textvariable=self.LotNo_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtLotNo.grid(row=4, column=1)

        lblIssueDate = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Issue Date :", padx=2)
        lblIssueDate.grid(row=5, column=0, sticky=tk.W)
        txtIssueDate = tk.Entry(DataFrameLeft,textvariable=self.issueDate_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtIssueDate.grid(row=5, column=1)

        lblExDate = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Exp Date :", padx=2)
        lblExDate.grid(row=6, column=0, sticky=tk.W)
        txtExDate = tk.Entry(DataFrameLeft,textvariable=self.expDate_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtExDate.grid(row=6, column=1)

        lblUses = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Uses :", padx=2)
        lblUses.grid(row=7, column=0, sticky=tk.W)
        txtUses = tk.Entry(DataFrameLeft,textvariable=self.uses_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtUses.grid(row=7, column=1)

        lblSideEffect = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Side Effect :", padx=2)
        lblSideEffect.grid(row=8, column=0, sticky=tk.W)
        txtSideEffect = tk.Entry(DataFrameLeft,textvariable=self.sideEffect_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtSideEffect.grid(row=8, column=1)

        lblPrecWarnig = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Prec&Warning :", padx=3)
        lblPrecWarnig.grid(row=0, column=2, sticky=tk.W)
        txtPrecWarnig = tk.Entry(DataFrameLeft,textvariable=self.pre_warning_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtPrecWarnig.grid(row=0, column=3)

        lblDosage = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Dosage :", padx=3)
        lblDosage.grid(row=1, column=2, sticky=tk.W)
        txtDosage = tk.Entry(DataFrameLeft,textvariable=self.dosage_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtDosage.grid(row=1, column=3)

        lblPrice = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Tablets Price :", padx=3)
        lblPrice.grid(row=2, column=2, sticky=tk.W)
        txtPrice = tk.Entry(DataFrameLeft,textvariable=self.price_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtPrice.grid(row=2, column=3)

        lblProductQt = tk.Label(DataFrameLeft, bg="#9cd6fb",foreground="#174487", font=("arial", 12, "bold"), text="Product QT :", padx=3)
        lblProductQt.grid(row=3, column=2, sticky=tk.W)
        txtProductQt = tk.Entry(DataFrameLeft,textvariable=self.productQt_var, font=("arial", 13, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtProductQt.grid(row=3, column=3)
        
        
        # Main Buttons
        btnAddData = tk.Button(ButtonFrame, text="Medicine Add",command=self.AddMed, font=("arial", 12, "bold"), bg="#006063",fg="#ffffff")
        btnAddData.grid(row=1, column=0, padx=5)

        btnUPdateData = tk.Button(ButtonFrame, text="Update", command=self.UpdateMed, font=("arial", 12, "bold"), bg="#cc3366", fg="white")
        btnUPdateData.grid(row=1, column=1, padx=5)

        btnDeleteData = tk.Button(ButtonFrame, text="Delete",command=self.DeleteMed, font=("arial", 12, "bold"), bg="#3074e1", fg="white")
        btnDeleteData.grid(row=1, column=2, padx=5)

        btnResetData = tk.Button(ButtonFrame, text="Reset",command=self.ClearMed, font=("arial", 12, "bold"), bg="#ff7a59", fg="white")
        btnResetData.grid(row=1, column=3, padx=5)

        btnExistData = tk.Button(ButtonFrame, text="Exit",command=self.iexit, font=("arial", 12, "bold"), bg="red", fg="white")
        btnExistData.grid(row=1, column=4, padx=5)

        lblSearch = tk.Label(ButtonFrame, font=("arial", 17, "bold"), text="Search By", padx=2, bg="#9cd6fb", fg="black")
        lblSearch.grid(row=1, column=5, sticky=tk.W, padx=5)



        serch_combo = ttk.Combobox(ButtonFrame,textvariable=self.search_var,width=17, font=("arial", 12, "bold"), state="readonly")
        serch_combo.grid(row=1, column=6, padx=5)
        serch_combo["values"] = ("Medname")
        serch_combo.grid(row=1, column=6, padx=5)
        serch_combo.current(0)

        txtSerch = tk.Entry(ButtonFrame,textvariable=self.txtsearch_var, bd=3, relief=tk.RIDGE, width=17, font=("arial", 17, "bold"))
        txtSerch.grid(row=1, column=7, padx=5)

        searchBtn = tk.Button(ButtonFrame,command=self.searchMed, text="SEARCH", font=("arial", 12, "bold"), bg="darkgreen", fg="white")
        searchBtn.grid(row=1, column=8, padx=5)

        showAll = tk.Button(ButtonFrame,text="SHOW ALL",command=self.fetch_Med, font=("arial", 12, "bold"), bg="#1b6592", fg="white")
        showAll.grid(row=1, column=9,padx=2,pady=10)

        main_menu = tk.Button(ButtonFrame,text="Main Menu",command=self.main_menu , font=("arial", 12, "bold"), bg="#ff6700", fg="white")
        main_menu.grid(row=1, column=10,padx=2,pady=10)

        


        

        # DataFrameRight
        DataFrameRight = tk.LabelFrame(DataFrame, bg="#9cd6fb", bd=0, relief=tk.RIDGE, padx=20, text="Medicine Add Department",
                                       fg="#273736", font=("arial", 25, "bold"))
        DataFrameRight.place(x=970, y=5, width=500, height=350)

        lblrefno = tk.Label(DataFrameRight, bg="#9cd6fb", font=("arial", 12, "bold"), text="Reference No :", padx=3)
        lblrefno.place(x=0, y=40)
        txtrefno = tk.Entry(DataFrameRight, textvariable=self.refNoDown_var, font=("arial", 13, "bold"), bg="white",
                            bd=2, relief=tk.RIDGE, width=29)
        txtrefno.place(x=135, y=40)

        lblmedName = tk.Label(DataFrameRight, bg="#9cd6fb", font=("arial", 12, "bold"), text="Medicine Name :", padx=3)
        lblmedName.place(x=0, y=70)
        txtmedName = tk.Entry(DataFrameRight, textvariable=self.medNameDown_var, font=("arial", 13, "bold"), bg="white",
                              bd=2, relief=tk.RIDGE, width=29)
        txtmedName.place(x=135, y=70)

        # Side frame
        side_frame = tk.Frame(DataFrameRight, bd=4, relief=tk.RIDGE, bg="white")
        side_frame.place(x=0, y=145, width=290, height=160)

        sc_x = ttk.Scrollbar(side_frame, orient=tk.HORIZONTAL)
        sc_x.pack(side=tk.BOTTOM, fill=tk.X)
        sc_y = ttk.Scrollbar(side_frame, orient=tk.VERTICAL)
        sc_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.medicine_table = ttk.Treeview(side_frame, column=("ref", "medname"), xscrollcommand=sc_x.set,
                                           yscrollcommand=sc_y.set)

        sc_x.config(command=self.medicine_table.xview)
        sc_y.config(command=self.medicine_table.yview)

        self.medicine_table.heading("ref", text="Ref")
        self.medicine_table.heading("medname", text="Medicine Name")

        self.medicine_table["show"] = "headings"
        self.medicine_table.pack(fill=tk.BOTH, expand=1)

        self.medicine_table.column("ref", width=100)
        self.medicine_table.column("medname", width=100)
        self.fetcdowmfrmae()
        self.medicine_table.bind("<ButtonRelease-1>",self.Medget_cursor)
        
        # Medicine add Button
        down_frame = tk.Frame(DataFrameRight, bd=4, relief=tk.RIDGE, bg="darkgreen")
        down_frame.place(x=320, y=149, width=135, height=139,)

        

        btnAddMed = tk.Button(down_frame,command=self.DownAddMed, text="ADD", font=("arial", 12, "bold"),height=1, width=12,
                              bg="lime", fg="white")
        btnAddMed.grid(row=0, column=0)

        btnUpdateData = tk.Button(down_frame,command=self.UpdateDownMed, text="Update", font=("arial", 12, "bold"),height=1, width=12, bg="#cc3366", fg="white")
        btnUpdateData.grid(row=1, column=0)

        btnDeleteData = tk.Button(down_frame,command=self.DownDeleteMed, text="Delete", font=("arial", 12, "bold"), width=12, bg="#3074e1", fg="white")
        btnDeleteData.grid(row=2, column=0)

        btnResetData = tk.Button(down_frame,command=self.DownClearMed, text="Reset", font=("arial", 12, "bold"), width=12, bg="#ff7a59", fg="white")
        btnResetData.grid(row=3, column=0)
        # Frame details
        Framedetails = tk.Frame(self.root, bd=10, relief=tk.RIDGE)
        Framedetails.place(x=0, y=590, width=1530, height=205)

        # Main table & Scrollbar
        Table_frame = tk.Frame(Framedetails, bd=15, relief=tk.RIDGE)
        Table_frame.place(x=0, y=1, width=1510, height=180)

        scroll_x = ttk.Scrollbar(Table_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y = ttk.Scrollbar(Table_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.pharmacy_table = ttk.Treeview(Table_frame,
                                           column=("ref", "companyname", "type", "tabletname", "lotno.", "issuedate",
                                                   "expdate", "uses", "sideeffect", "warning", "dosage", "price",
                                                   "productqt"),
                                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.pharmacy_table.xview)
        scroll_y.config(command=self.pharmacy_table.yview)

        self.pharmacy_table["show"] = "headings"

        self.pharmacy_table.heading("ref", text="Reference No")
        self.pharmacy_table.heading("companyname", text="Company Name")
        self.pharmacy_table.heading("type", text="Type of Medicine")
        self.pharmacy_table.heading("tabletname", text="Tablet Name")
        self.pharmacy_table.heading("lotno.", text="Lot No")
        self.pharmacy_table.heading("issuedate", text="Issue Date")
        self.pharmacy_table.heading("expdate", text="Exp Date")
        self.pharmacy_table.heading("uses", text="Uses")
        self.pharmacy_table.heading("sideeffect", text="Side Effect")
        self.pharmacy_table.heading("warning", text="Prec&Warning")
        self.pharmacy_table.heading("dosage", text="Dosage")
        self.pharmacy_table.heading("price", text="Price")
        self.pharmacy_table.heading("productqt", text="Product Qts")

        self.pharmacy_table.pack(fill=tk.BOTH, expand=1)

        self.pharmacy_table.column("ref", width=100)
        self.pharmacy_table.column("companyname", width=100)
        self.pharmacy_table.column("type", width=100)
        self.pharmacy_table.column("tabletname", width=100)
        self.pharmacy_table.column("lotno.", width=100)
        self.pharmacy_table.column("issuedate", width=100)
        self.pharmacy_table.column("expdate", width=100)
        self.pharmacy_table.column("uses", width=100)
        self.pharmacy_table.column("sideeffect", width=100)
        self.pharmacy_table.column("warning", width=100)
        self.pharmacy_table.column("dosage", width=100)
        self.pharmacy_table.column("price", width=100)
        self.pharmacy_table.column("productqt", width=100)
        self.pharmacy_table.bind("<ButtonRelease-1>",self.getCursor)
        self.fetch_Med()


    def DownAddMed(self):
        conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
        my_cursor = conn.cursor()
        sql = "INSERT INTO pharma (Ref,MedName) VALUES (%s,%s)"
        val = (self.refNoDown_var.get(),
               self.medNameDown_var.get())
        my_cursor.execute(sql, val)
        conn.commit()
        self.fetcdowmfrmae()
        self.Medget_cursor()
        conn.close()
        messagebox.showinfo('Success', "Medicine Name added", parent=self.root)
        

    def AddMed(self):
        conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
        my_cursor = conn.cursor()
        sql = "INSERT INTO my_pharma (ref, companyName, type, tabletname, lotno, issuedate, expdate, uses, sideeffects, warning, dosage, price, productqt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (self.refMed_var.get(),
            self.companyName_var.get(),
            self.typeMed_var.get(),
            self.tabletName_var.get(),
            self.LotNo_var.get(),
            self.issueDate_var.get(),
            self.expDate_var.get(),
            self.uses_var.get(),
            self.sideEffect_var.get(),
            self.pre_warning_var.get(),
            self.dosage_var.get(),
            self.price_var.get(),
            self.productQt_var.get())
                
        my_cursor.execute(sql, val)
        conn.commit()
        self.fetch_Med()
        conn.close()
        messagebox.showinfo('Success', "Medicine Name added", parent=self.root)


    def fetch_Med(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM my_pharma")
            row = my_cursor.fetchall()
            if len(row) != 0:
                self.pharmacy_table.delete(*self.pharmacy_table.get_children())
                for i in row:
                    self.pharmacy_table.insert("", "end", values=i)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

    def fetcdowmfrmae(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM pharma")
            row = my_cursor.fetchall()
            if len(row) != 0:
                self.medicine_table.delete(*self.medicine_table.get_children())
                for i in row:
                    self.medicine_table.insert("", "end", values=i)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

    
    def Medget_cursor(self,event=""):
        cursor_row=self.medicine_table.focus()
        content=self.medicine_table.item(cursor_row)
        row=content["values"]
        self.refNoDown_var.set(row[0])
        self.medNameDown_var.set(row[1])

    def UpdateDownMed(self):
        conn = None
        my_cursor = None
        
        try:
            if self.refNoDown_var.get() == "" or self.medNameDown_var.get() == "":
                messagebox.showerror("Error", "All fields are required")
            else:
                conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
                my_cursor = conn.cursor()
                query = "UPDATE pharma SET MedName = %s WHERE Ref = %s"
                data = (self.medNameDown_var.get(), self.refNoDown_var.get())
                my_cursor.execute(query, data)
                conn.commit()
                self.fetcdowmfrmae()
                messagebox.showinfo('Success', "Medicine Name updated", parent=self.root)
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror('Error', f"An error occurred: {e}", parent=self.root)
        finally:
            if my_cursor is not None:
                my_cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()
                

    def DownDeleteMed(self):
        conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
        my_cursor = conn.cursor()
        query = "delete from pharma WHERE Ref = %s"
        data = (self.refNoDown_var.get(),)
        my_cursor.execute(query, data)
        conn.commit()
        self.fetcdowmfrmae()
        messagebox.showinfo('Success', "Record Deleted", parent=self.root)
  


    def DownClearMed(self):
        self.medNameDown_var.set("")
        self.refNoDown_var.set("")

    def getCursor(self,ev=""):
        cursor_row=self.pharmacy_table.focus()
        content=self.pharmacy_table.item(cursor_row)
        row=content["values"]
        self.refMed_var.set(row[0]),
        self.companyName_var.set(row[1]),
        self.typeMed_var.set(row[2]),
        self.tabletName_var.set(row[3]),
        self.LotNo_var.set(row[4]),
        self.issueDate_var.set(row[5]),
        self.expDate_var.set(row[6]),
        self.uses_var.set(row[7]),
        self.sideEffect_var.set(row[8]),
        self.pre_warning_var.set(row[9]),
        self.dosage_var.set(row[10]),
        self.price_var.set(row[11]),
        self.productQt_var.set(row[12])

    def UpdateMed(self):
        conn = None
        my_cursor = None
        
        try:
            
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            query = "UPDATE my_pharma SET companyName=%s, type=%s, tabletname=%s, lotno=%s, issuedate=%s, expdate=%s, uses=%s, sideeffects=%s, warning=%s, dosage=%s, price=%s, productqt=%s where ref=%s"
            data = (self.companyName_var.get(),
                     self.typeMed_var.get(),
                     self.tabletName_var.get(),
                     self.LotNo_var.get(),
                     self.issueDate_var.get(),
                     self.expDate_var.get(),
                     self.uses_var.get(),
                     self.sideEffect_var.get(),
                     self.pre_warning_var.get(),
                     self.dosage_var.get(),
                     self.price_var.get(),
                     self.productQt_var.get(),
                     self.refMed_var.get())
        
            my_cursor.execute(query, data)
            conn.commit()
            self.fetch_Med()
            messagebox.showinfo('Success', "Medicine updated", parent=self.root)
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror('Error', f"An error occurred: {e}", parent=self.root)
        finally:
            if my_cursor is not None:
                my_cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    def DeleteMed(self):
        conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
        my_cursor = conn.cursor()
        query = "delete from my_pharma WHERE ref = %s"
        data = (self.refMed_var.get(),)
        my_cursor.execute(query, data)
        conn.commit()
        self.fetch_Med()
        messagebox.showinfo('Success', "Record Deleted", parent=self.root)
  


    def ClearMed(self):
        self.refMed_var.set(""),
        self.companyName_var.set(""),
        self.typeMed_var.set(""),
        self.tabletName_var.set(""),
        self.LotNo_var.set(""),
        self.issueDate_var.set(""),
        self.expDate_var.set(""),
        self.uses_var.set(""),
        self.sideEffect_var.set(""),
        self.pre_warning_var.set(""),
        self.dosage_var.set(""),
        self.price_var.set(""),
        self.productQt_var.set("")

    def searchMed(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            search_value = self.txtsearch_var.get()
            query = "SELECT * FROM my_pharma WHERE tabletname LIKE %s"
            my_cursor.execute(query, (f"%{search_value}%",))
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.pharmacy_table.delete(*self.pharmacy_table.get_children())
                for i in rows:
                    self.pharmacy_table.insert("", "end", values=i)
            else:
                messagebox.showinfo('No Results', "No matching records found", parent=self.root)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror('Error', f"An error occurred: {e}", parent=self.root)
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()
    
    def main_menu(self):
        self.root.withdraw()   # hide current window
        new_window = Toplevel()
        app = Main_Menu(new_window)


    def iexit(self):   
        self.root.destroy()

class Billing:
        
    def __init__(self,root):
        self.root=root
        self.root.title("MENU")
        self.root.geometry("1600x900+0+0")
        #Variables
        self.name_var = tk.StringVar() 
        self.contact_var = tk.IntVar() 
        self.refMed_var = tk.StringVar()
        self.tabletName_var = tk.StringVar()
        self.dosage_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.amount_var=tk.StringVar()
        self.grandTotal_var=tk.IntVar()
        self.Reset()
        

        billing_lbl= Label(text="- - - - - Billing System - - - - -",font=("Arial",20,"bold"))
        billing_lbl.place(x=0,y=10,width=1600, height=50)
        
        DataFrame = tk.Frame(self.root, bd=0, bg="#9cd6fb",relief=tk.RIDGE, padx=20, pady=50)
        DataFrame.place(x=70, y=70, width=1400, height=690)

        
        name = Label(DataFrame, text="Name ", font=("arial", 15, "bold"), fg="black", bg="#9cd6fb",pady=10)
        name.grid(row=0,column=0, sticky=tk.W)
        name = ttk.Entry(DataFrame,textvariable=self.name_var , font=("arial", 15, "bold"),)
        name.grid(row=0, column=1)

        contact = Label(DataFrame, text="Contact No. ", font=("arial", 15, "bold"), fg="black", bg="#9cd6fb",pady=10)
        contact.grid(row=1,column=0,sticky=tk.W)
        contact = ttk.Entry(DataFrame,textvariable=self.contact_var , font=("arial", 15, "bold"))
        contact.grid(row=1, column=1)

        #search variables
        self.search_var=tk.StringVar()  
        #search txt variable
        self.txtsearch_var=tk.StringVar()

        search_lbl = Label(DataFrame, text="Search by", font=("arial", 15, "bold"), fg="black", bg="#9cd6fb",pady=10)
        search_lbl.grid(row=2,column=0,sticky=tk.W)

        serch_combo = ttk.Combobox(DataFrame,textvariable=self.search_var,width=17, font=("arial", 12, "bold"), state="readonly")
        serch_combo.grid(row=3, column=0, padx=5)
        serch_combo["values"] = ("ref","Medname")
        serch_combo.grid(row=3, column=0, padx=5)
        serch_combo.current(0)
        txtSerch = tk.Entry(DataFrame,textvariable=self.txtsearch_var, relief=tk.RIDGE, font=("arial", 15, "bold"))
        txtSerch.grid(row=3, column=1, padx=5)
        searchBtn = tk.Button(DataFrame,command=self.searchMed, text="SEARCH", font=("arial", 12, "bold"), bg="darkgreen", fg="white")
        searchBtn.grid(row=4, column=0, padx=5)
        showAll = tk.Button(DataFrame,text="SHOW ALL",command=self.fetch_Med, font=("arial", 12, "bold"), bg="#1b6592", fg="white")
        showAll.grid(row=4, column=1,padx=2,pady=50)

              
                # Tablet Name Label and Entry
        lblTabletName = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 12, "bold"), text="Tablet Name:", padx=2, pady=6)
        lblTabletName.grid(row=5, column=0, sticky=tk.W)

        txtTabletName = tk.Entry(DataFrame, textvariable=self.tabletName_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtTabletName.grid(row=5, column=1)

        # Dose Label and Entry
        lblDose = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 12, "bold"), text="Dose:", padx=2, pady=6)
        lblDose.grid(row=6, column=0, sticky=tk.W)

        txtDose = tk.Entry(DataFrame, textvariable=self.dosage_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtDose.grid(row=6, column=1)

        # Rate Label and Entry
        lblRate = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 12, "bold"), text="Rate:", padx=2, pady=6)
        lblRate.grid(row=7, column=0, sticky=tk.W)

        txtRate = tk.Entry(DataFrame, textvariable=self.price_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtRate.grid(row=7, column=1)

        # Quantity Label and Entry
        lblQuantity = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 12, "bold"), text="Quantity:", padx=2, pady=6)
        lblQuantity.grid(row=8, column=0, sticky=tk.W)

        txtQuantity = tk.Entry(DataFrame, textvariable=self.quantity_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        txtQuantity.grid(row=8, column=1)
        txtQuantity.bind("<FocusOut>", lambda event: self.update_amount())

        # Amount Label and Entry
        # lblAmount = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 12, "bold"), text="Amount:", padx=2, pady=6)
        # lblAmount.grid(row=9, column=0, sticky=tk.W)

        # txtAmount = tk.Entry(DataFrame, textvariable=self.amount_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=29)
        # txtAmount.grid(row=9, column=1)

        # Add Medicine Button

        btnAddMed = tk.Button(DataFrame,command=self.AddToBillInfo, text="Add Medicine", font=("arial", 12, "bold"), bg="darkgreen", fg="white")
        btnAddMed.grid(row=10, column=0, padx=5,pady=10)

        # Remove Medicine Button
        btnRemoveMed = tk.Button(DataFrame,command=self.RemoveFromBillInfo, text="Remove Medicine", font=("arial", 12, "bold"), bg="darkgreen", fg="white")
        btnRemoveMed.grid(row=10, column=1, pady=10,padx=5)

        # Refresh BillInfo Table 
        btnReset = tk.Button(DataFrame,command=self.Reset, text="Reset", font=("arial", 12, "bold"), bg="darkgreen", fg="white")
        btnReset.grid(row=11, column=0, pady=10,padx=5)

        btndeleteAll = tk.Button(DataFrame,command=self.clearBillInfoTable, text="Delete all", font=("arial", 12, "bold"), bg="darkgreen", fg="white")
        btndeleteAll.grid(row=11, column=1, pady=10,padx=5)

        
        btnPrintBill = tk.Button(DataFrame,command=self.createBillPDF, text="Print Bill", font=("arial", 12, "bold"), bg="Pink", fg="white")
        btnPrintBill.grid(row=12, column=0, pady=10,padx=5)

        main_menu = tk.Button(DataFrame,text="Main Menu",command=self.main_menu , font=("arial", 12, "bold"), bg="#ff6700", fg="white")
        main_menu.grid(row=12, column=1,padx=2,pady=10)


        lblPharmaTable = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 15, "bold"), text="Pharma Table", padx=2, pady=6)
        lblPharmaTable.place(x=620,y=-35)
        
        
        Table_frame = tk.Frame(DataFrame, bd=15, relief=tk.RIDGE)
        Table_frame.place(x=600, y=0, width=700, height=180)

        scroll_x = ttk.Scrollbar(Table_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y = ttk.Scrollbar(Table_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.pharmacy_table = ttk.Treeview(Table_frame,
                                           column=("ref","tabletname","dosage", "price","productqt"),
                                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.pharmacy_table.xview)
        scroll_y.config(command=self.pharmacy_table.yview)

        self.pharmacy_table["show"] = "headings"

        self.pharmacy_table.heading("ref", text="Reference No")
        self.pharmacy_table.heading("tabletname", text="Tablet Name")
        self.pharmacy_table.heading("dosage", text="Dosage")
        self.pharmacy_table.heading("price", text="Price")
        self.pharmacy_table.heading("productqt", text="Product Qts")

        self.pharmacy_table.pack(fill=tk.BOTH, expand=1)

        self.pharmacy_table.column("ref", width=100)
        self.pharmacy_table.column("tabletname", width=100)
        self.pharmacy_table.column("dosage", width=100)
        self.pharmacy_table.column("price", width=100)
        self.pharmacy_table.column("productqt", width=100)
        self.pharmacy_table.bind("<ButtonRelease-1>",self.FillEntryFields)
        self.fetch_Med()


        lblCustomTable = tk.Label(DataFrame, bg="#9cd6fb", foreground="#174487", font=("arial", 15, "bold"), text="Custom Table", padx=2, pady=6)
        lblCustomTable.place(x=620,y=250)
        
        lblGrandTotal = tk.Label(DataFrame, bg="#9cd6fb", foreground="Green", font=("arial", 12, "bold"), text="Grand Total", padx=2, pady=6)
        lblGrandTotal.place(x=1010,y=595)
        
        txtGrandTotal = tk.Entry(DataFrame, textvariable=self.grandTotal_var, font=("arial", 12, "bold"), bg="white", bd=2, relief=tk.RIDGE, width=20)
        txtGrandTotal.place(x=1112,y=601,)
        
        Table_frame = tk.Frame(DataFrame, bd=15, relief=tk.RIDGE)
        Table_frame.place(x=600, y=300, width=700, height=300)

        scroll_x = ttk.Scrollbar(Table_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y = ttk.Scrollbar(Table_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.custom_table = ttk.Treeview(Table_frame,
                                        column=("Tablet Name", "Dose", "Rate", "Quantity","Amount"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.custom_table.xview)
        scroll_y.config(command=self.custom_table.yview)

        self.custom_table["show"] = "headings"

        self.custom_table.heading("Tablet Name", text="Tablet Name")
        self.custom_table.heading("Dose", text="Dose")
        self.custom_table.heading("Rate", text="Rate")
        self.custom_table.heading("Quantity", text="Quantity")
        self.custom_table.heading("Amount", text="Amount")

        self.custom_table.pack(fill=tk.BOTH, expand=1)


        self.custom_table.column("Tablet Name", width=200)
        self.custom_table.column("Dose", width=110)
        self.custom_table.column("Rate", width=90)
        self.custom_table.column("Quantity", width=90)
        self.custom_table.column("Amount", width=90)

        self.custom_table.bind("<ButtonRelease-1>",self.FillBillInfoEntryFields)  # Update to your actual event handler
        self.fetch_and_display_data()
         # Update to your actual data fetching function



    def fetch_Med(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT ref, tabletname, dosage, price,productqt FROM my_pharma")
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.pharmacy_table.delete(*self.pharmacy_table.get_children())
                for row in rows:
                    self.pharmacy_table.insert("", "end", values=row)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

    
    def Reset(self):
        self.tabletName_var.set(""),
        self.dosage_var.set(""),
        self.price_var.set(""),
        self.quantity_var.set(""),
        self.amount_var.set("")



    def searchMed(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            search_value = self.txtsearch_var.get()
            query = "SELECT ref, tabletname, dosage, price FROM my_pharma WHERE  ref LIKE %s OR tabletname LIKE %s"
            my_cursor.execute(query, (f"%{search_value}%",f"%{search_value}%"))
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.pharmacy_table.delete(*self.pharmacy_table.get_children())
                for i in rows:
                    self.pharmacy_table.insert("", "end", values=i)
            else:
                messagebox.showinfo('No Results', "No matching records found", parent=self.root)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror('Error', f"An error occurred: {e}", parent=self.root)
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()
        
    def FillEntryFields(self, event=""):
        cursor_row = self.pharmacy_table.focus()
        content = self.pharmacy_table.item(cursor_row)
        row = content["values"]

        # Assuming the order is ref, tabletName, dosage, price, productQt
        self.tabletName_var.set(row[1])
        self.dosage_var.set(row[2])
        self.price_var.set(row[3])
    

    def fetch_and_display_data(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()

            my_cursor.execute("SELECT TabletName, Dose, Rate, Quantity, Amount FROM billinfo")
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.custom_table.delete(*self.custom_table.get_children())
                for row in rows:
                    self.custom_table.insert("", "end", values=row)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()


    def AddToBillInfo(self):
        self.update_amount()
        self.current_datetime = datetime.now().strftime("%Y-%m-%d")

        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()

            sql = "INSERT INTO billinfo (Date,TabletName, Dose, Rate, Quantity, Amount) VALUES (%s,%s, %s, %s, %s, %s)"
            val = (
                self.current_datetime,
                self.tabletName_var.get(),
                self.dosage_var.get(),
                self.price_var.get(),
                self.quantity_var.get(),
                self.amount_var.get()
            )

            my_cursor.execute(sql, val)
            self.calculateGrandTotal()
            conn.commit()
            self.fetch_and_display_data()
            self.Reset()
            #messagebox.showinfo("Success", "Medicine added successfully!")

            # Additional logic if needed after the data is inserted

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            # Handle the error as needed, e.g., show an error message to the user

        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()



    
    def RemoveFromBillInfo(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()

            sql = "DELETE FROM billinfo WHERE tabletName = %s"
            val = (self.tabletName_var.get(),)

            my_cursor.execute(sql, val)
            conn.commit()

            # Clear existing data in the custom_table
            for row_id in self.custom_table.get_children():
                self.custom_table.delete(row_id)
                self.calculateGrandTotal()
            # Fetch and display data in custom_table after removing medicine
            self.fetch_and_display_data()
            self.Reset()

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            # Handle the error as needed, e.g., show an error message to the user

        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

    

    def clearBillInfoTable(self):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="dhruvp@70441",
                database="mydata"
            )
            my_cursor = conn.cursor()

            # Clear all rows from the billinfo table
            my_cursor.execute("DELETE FROM billinfo")
            conn.commit()

            # Clear existing data in the custom_table
            for row_id in self.custom_table.get_children():
                self.custom_table.delete(row_id)

            # Update the grand total after clearing the table
            self.calculateGrandTotal()
            self.Reset()

        except mysql.connector.Error as e:
            print(f"Error clearing billinfo table: {e}")

        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

    # Example usage:
    # Call this function whenever you want to clear the billinfo table and update the custom_table and grand total
    # self.clearBillInfoTable()






    def FillBillInfoEntryFields(self, event=""):
        cursor_row = self.custom_table.focus()
        content = self.custom_table.item(cursor_row)
        row = content["values"]

        # Assuming the order is Tablet Name, Dose, Rate, Quantity, Amount
        self.tabletName_var.set(row[0])
        self.dosage_var.set(row[1])
        self.price_var.set(row[2])
        self.quantity_var.set(row[3])
        self.amount_var.set(row[4])



    def update_amount(self, event=""):
        try:
            quantity_str = self.quantity_var.get()
            price_str = self.price_var.get()

            # Check if both quantity and price are numeric strings
            if quantity_str.isdigit() and price_str.isdigit():
                quantity = int(quantity_str)
                price = int(price_str)

                amount = quantity * price
                self.amount_var.set(amount)
            else:
                # Handle the case where either quantity or price is not a valid number
                # You can display an error message or take appropriate action
                pass
        except ValueError:
            # Handle non-numeric input gracefully
            pass

    # def calculateGrandTotal(self):
    #     total = 0
    #     for item in self.custom_table.get_children():
    #         amount = int(self.custom_table.item(item, 'values')[4])  # Assuming Amount is in the fifth column
    #         total += amount

    #     self.grandTotal_var.set(total)


    def calculateGrandTotal(self):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="dhruvp@70441",
                database="mydata"
            )
            my_cursor = conn.cursor()

            # Calculate the sum of Amount column in billinfo table
            my_cursor.execute("SELECT SUM(Amount) FROM billinfo")
            total = my_cursor.fetchone()[0] or 0  # If the result is None, set total to 0

            self.grandTotal_var.set(total)

        except mysql.connector.Error as e:
            print(f"Error calculating total: {e}")

        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

            # Call the function again after a delay (e.g., every 1000 milliseconds or 0.5 second)
            self.root.after(500, self.calculateGrandTotal)


    def createBillPDF(self):
        #========================copy billifo to sales table================
    
        try:
            # Connect to the database
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="dhruvp@70441",
                database="mydata"
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Select data from the billinfo table
            cursor.execute("SELECT Date, TabletName, Dose, Rate, Quantity, Amount FROM billinfo")

            # Fetch all rows
            rows = cursor.fetchall()
            bill_number = self.generate_bill_number()
            # Insert fetched data into the sales table
            for row in rows:
                date, tablet_name, dose, rate, quantity, amount = row

                insert_query = "INSERT INTO sales (Date, Bill_No, TabletName, Dose, Rate, Quantity, Amount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (date, bill_number, tablet_name, dose, rate, quantity, amount)
                cursor.execute(insert_query, values)

            # Commit changes
            conn.commit()

            # Close cursor and connection
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error: {e}")

        
        try:
            # Get values from instance variables
            customer_name = str(self.name_var.get())
            contact_number = str(self.contact_var.get())

            # Generate unique bill number
            bill_number = self.generate_bill_number()

            # Get current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Create a PDF document
            pdf_filename = "bill.pdf"
            pdf = FPDF()
            pdf.add_page()

            # Set left margin
            pdf.set_left_margin(5)

            # Set right margin
            pdf.set_right_margin(5)

            # Add bill number, date, and time to the PDF
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 10, txt=f"Bill No: {bill_number}", ln=True, align='R')
            pdf.cell(0, 10, txt=f"Date: {current_datetime}", ln=True, align='R')

            # Add Medicine Bill title
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(0, 10, txt="--- Medicine Bill ---", ln=True, align='C')

            # Set font
            pdf.set_font("Arial", size=12)

            # Add Name and contact number to the PDF
            pdf.cell(200, 10, txt=f"Name: {customer_name}", ln=True)
            pdf.cell(200, 10, txt=f"Contact Number: {contact_number}", ln=True)
            pdf.ln(10)  # Add some space between Name/Contact and the table

            # Create a table with the bill info
            bill_info_table = self.fetch_bill_info_from_database()

            # Set font for table headings
            pdf.set_font("Arial", style='B', size=10)

            # Define column headings
            headings = ["Tablet Name", "Dose", "Rate", "Quantity", "Amount"]
            
            # Define column widths
            col_widths = [70, 30, 30, 30, 40]

            # Add headings to the table
            for heading, width in zip(headings, col_widths):
                pdf.cell(width, 10, txt=heading, border=1)

            pdf.ln()

            # Set font for table content
            pdf.set_font("Arial", size=10)

            # Add rows to the table
            for row in bill_info_table:
                for col, width in zip(row, col_widths):
                    pdf.cell(width, 10, txt=str(col), border=1)
                pdf.ln()

            # Set font for Grand Total
            pdf.set_font("Arial", style='B', size=14)

            # Add grand total to the PDF
            pdf.cell(200, 10, txt=f"\nGrand Total: {str(self.grandTotal_var.get())}", ln=True, align='R')

            # Save the PDF
            pdf.output(pdf_filename)

            messagebox.showinfo("PDF Generated", "PDF is generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error creating Bill PDF: {e}")

        


        def generate_bill_number(self):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Get current timestamp
            return f"BILL-{timestamp}"
            

    def fetch_bill_info_from_database(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="dhruvp@70441", database="mydata")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT TabletName, Dose, Rate, Quantity, Amount FROM billinfo")
            bill_info_data = my_cursor.fetchall()
            return bill_info_data
        except mysql.connector.Error as e:
            print(f"Error fetching bill info from database: {e}")
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()

    def main_menu(self):
        self.root.withdraw()   # hide current window
        new_window = Toplevel()
        app = Main_Menu(new_window)


class Report:
    def __init__(self, root):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="dhruvp@70441",
            database="mydata"
        )

        query = "SELECT * FROM sales"
        self.df = pd.read_sql(query, self.conn)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Amount'] = pd.to_numeric(self.df['Amount'])
        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'])

        self.root = root
        self.root.title("Sales Dashboard")
        self.root.geometry("1200x800")

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=BOTH, expand=1)

        self.page1 = Frame(self.notebook)
        self.page2 = Frame(self.notebook)
        
        self.notebook.add(self.page1, text="Page 1")
        self.notebook.add(self.page2, text="Page 2")

        self.chart_frames = []
        for page in [self.page1, self.page2]:
            for i in range(2):
                for j in range(2):
                    frame = Frame(page, bg='white', padx=5, pady=5)
                    frame.grid(row=i, column=j, sticky=NSEW)
                    page.grid_rowconfigure(i, weight=1)
                    page.grid_columnconfigure(j, weight=1)
                    self.chart_frames.append(frame)

        # Date range inputs
        date_frame = Frame(self.main_frame, bg='#add8e6', padx=10, pady=10)
        date_frame.pack(fill=X)

        Label(date_frame, text="Starting Date (YYYY-MM-DD)", bg='#add8e6').pack(side=LEFT, padx=5)
        self.start_date_entry = Entry(date_frame)
        self.start_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="Ending Date (YYYY-MM-DD)", bg='#add8e6').pack(side=LEFT, padx=5)
        self.end_date_entry = Entry(date_frame)
        self.end_date_entry.pack(side=LEFT, padx=5)

        # Update Charts button
        button_frame = Frame(self.main_frame, bg='#add8e6', padx=10, pady=10)
        button_frame.pack(fill=X)

        ttk.Button(button_frame, text="Update Charts", command=self.update_charts).pack(side=LEFT, padx=10)

        self.chart_types = ['line', 'bar']
        self.chart_type_buttons = []

        # Chart type toggle buttons
        for frame in self.chart_frames:
            toggle_frame = Frame(frame, bg='white')
            toggle_frame.pack(side=TOP, fill=X)
            for chart_type in self.chart_types:
                btn = ttk.Button(toggle_frame, text=chart_type.capitalize(), command=lambda ctype=chart_type: self.update_charts(ctype))
                btn.pack(side=LEFT, padx=5)
                self.chart_type_buttons.append(btn)

    def format_large_values(self, value, pos):
        if value >= 1_000_000:
            return f'{value / 1_000_000:.1f}M'
        elif value >= 1_000:
            return f'{value / 1_000:.1f}k'
        else:
            return str(value)

    def filter_data(self, start_date, end_date):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]
        return filtered_df

    def update_charts(self, chart_type='line'):
        self.clear_canvases()

        self.create_plot(self.chart_frames[0], 'Sales Over Time', self.plot_sales_over_time, chart_type)
        self.create_plot(self.chart_frames[1], 'Quantity Over Time', self.plot_quantity_over_time, chart_type)
        self.create_plot(self.chart_frames[2], 'Top Medicines', self.plot_top_meds, 'bar')
        self.create_plot(self.chart_frames[3], 'Top Selling Days', self.plot_top_selling_days, 'bar')

        self.create_plot(self.chart_frames[4], 'Top Medicines Contribution', self.plot_top_meds_pie, 'pie')
        self.create_plot(self.chart_frames[5], 'Rate vs Quantity', self.plot_rate_vs_quantity, 'scatter')

    def create_plot(self, frame, title, plot_func, plot_type):
        fig, ax = plt.subplots(figsize=(5, 4))
        plot_func(ax, plot_type)
        ax.set_title(title)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'{sel.artist.get_ydata()[sel.target.index]:.1f}'))

    def plot_sales_over_time(self, ax, plot_type):
        filtered_df = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).resample('M', on='Date').sum()
        filtered_df['Amount'].plot(ax=ax, kind=plot_type, color='blue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales Amount')
        ax.get_yaxis().set_major_formatter(FuncFormatter(self.format_large_values))
        ax.legend(['Sales Amount'])
        plt.xticks(rotation=45)

    def plot_quantity_over_time(self, ax, plot_type):
        filtered_df = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).resample('M', on='Date').sum()
        filtered_df['Quantity'].plot(ax=ax, kind=plot_type, color='green')
        ax.set_xlabel('Date')
        ax.set_ylabel('Quantity Sold')
        ax.get_yaxis().set_major_formatter(FuncFormatter(self.format_large_values))
        ax.legend(['Quantity Sold'])
        plt.xticks(rotation=45)

    def plot_top_meds(self, ax, plot_type):
        top_meds = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).groupby('TabletName')['Quantity'].sum().nlargest(10)
        top_meds.plot(kind='bar', ax=ax, color='purple')
        ax.set_xlabel('Medicine')
        ax.set_ylabel('Quantity Sold')
        ax.get_yaxis().set_major_formatter(FuncFormatter(self.format_large_values))
        ax.legend(['Quantity Sold'])
        plt.xticks(rotation=45, ha='right')

    def plot_top_meds_pie(self, ax, plot_type):
        top_meds = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).groupby('TabletName')['Quantity'].sum().nlargest(10)
        top_meds.plot(kind='pie', ax=ax, autopct='%1.1f%%')

    def plot_top_selling_days(self, ax, plot_type):
        top_days = self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()).groupby('Date')['Amount'].sum().nlargest(10)
        top_days.plot(kind='bar', ax=ax, color='orange')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales Amount')
        ax.get_yaxis().set_major_formatter(FuncFormatter(self.format_large_values))
        ax.legend(['Sales Amount'])
        plt.xticks(rotation=45)

    def plot_rate_vs_quantity(self, ax, plot_type):
        sns.histplot(data=self.filter_data(self.start_date_entry.get(), self.end_date_entry.get()), x='Rate', y='Quantity', ax=ax)
        ax.set_title('Rate vs Quantity Sold')
        ax.set_xlabel('Rate')
        ax.set_ylabel('Quantity Sold')

    def clear_canvases(self):
        for frame in self.chart_frames:
            for widget in frame.winfo_children():
                widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Report(root)
    root.mainloop()







if __name__ == "__main__":
    main()

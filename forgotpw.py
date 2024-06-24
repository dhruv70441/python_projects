from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class forgotpassword:
    def __init__(self,root) -> None:
        self.root = root
        self.root.title("Reset Password")
        self.root.geometry("1600x900+0+0")


        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()
        

        frame = Frame(self.root, bg="white")
        frame.place(x=400, y=100, width=800, height=550)

        email = Label(frame, text="Email", font=("arial", 15, "bold"), bg="white")
        email.place(x=50, y=200)
        email = ttk.Entry(frame, textvariable=self.var_email, font=("arial", 15, "bold"))
        email.place(x=240, y=200, width=250)

        password = Label(frame, text="New Password:", font=("arial", 15, "bold"), bg="white")
        password.place(x=50, y=250)
        password = Entry(frame, textvariable=self.var_pass, font=("arial", 15, "bold"), width=19, show="*")
        password.place(x=240, y=250, width=250)

        confpassword = Label(frame, text="Confirm New Password:", font=("arial", 15, "bold"), bg="white")
        confpassword.place(x=50, y=300)
        conf_password = Entry(frame, textvariable=self.var_confpass, font=("arial", 15, "bold"), width=19, show="*")
        conf_password.place(x=240, y=300, width=250)

        update_btn = Button(frame, text="Update Password", command=self.update_pass, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="white", activebackground="white", activeforeground="gray")
        update_btn.place(x=255, y=450, height=50, width=100)

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



if __name__ == "__main__":
    root = Tk()
    app = forgotpassword(root)
    root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
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

        frame = Frame(self.root, bg="white")
        frame.place(x=400, y=100, width=800, height=550)

        fname = Label(frame, text="First Name", font=("arial", 15, "bold"), bg="white")
        fname.place(x=50, y=100)
        fname = ttk.Entry(frame, textvariable=self.var_fname, font=("arial", 15, "bold"))
        fname.place(x=240, y=100, width=250)

        lname = Label(frame, text="Last Name", font=("arial", 15, "bold"), bg="white")
        lname.place(x=50, y=150)
        lname = ttk.Entry(frame, textvariable=self.var_lname, font=("arial", 15, "bold"))
        lname.place(x=240, y=150, width=250)

        email = Label(frame, text="Email", font=("arial", 15, "bold"), bg="white")
        email.place(x=50, y=200)
        email = ttk.Entry(frame, textvariable=self.var_email, font=("arial", 15, "bold"))
        email.place(x=240, y=200, width=250)

        password = Label(frame, text="Password:", font=("arial", 15, "bold"), bg="white")
        password.place(x=50, y=250)
        password = Entry(frame, textvariable=self.var_pass, font=("arial", 15, "bold"), width=19, show="*")
        password.place(x=240, y=250, width=250)

        confpassword = Label(frame, text="Confirm Password:", font=("arial", 15, "bold"), bg="white")
        confpassword.place(x=50, y=300)
        conf_password = Entry(frame, textvariable=self.var_confpass, font=("arial", 15, "bold"), width=19, show="*")
        conf_password.place(x=240, y=300, width=250)

        Checkbtn = Checkbutton(frame, text="I Agree the Terms & Conditions", variable=self.var_check, font=("arial", 10, "bold"), background="white", onvalue=1, offvalue=0)
        Checkbtn.place(x=240, y=400)

        register_btn = Button(frame, text="Register", command=self.register_data, font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="white", activebackground="white", activeforeground="gray")
        register_btn.place(x=255, y=450, height=50, width=100)

        login_btn = Button(frame, text="Login", font=("arial", 15, "bold"), bd=0, relief=RIDGE, fg="black", bg="white", activebackground="white", activeforeground="gray")
        login_btn.place(x=455, y=450, height=50, width=100)

        
    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "":
            messagebox.showerror("Error", "Please enter name and email")
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error", "PASSWORD and CONFIRM PASSWORD must be the same")
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to the terms and conditions")
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
if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()

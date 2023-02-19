from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
 
 
root = Tk()
root.title("Login")
root.config(bg="#181100" )
# root.grid_rowconfigure(1, weight=1)
# root.grid_columnconfigure(0,weight=1)
root.iconbitmap("img/enter.ico")
root.geometry("600x400")

# user image
user_img = Image.open("img/user-white.png")
resize_img = user_img.resize((35,35))
update_user = ImageTk.PhotoImage(resize_img)

# password image
pass_img = Image.open("img/lock-white.png")
resize_pass_img = pass_img.resize((35,35))
update_pass = ImageTk.PhotoImage(resize_pass_img)



def login():

    get_username = username.get()
    get_password = password.get()

    if get_username == "admin" and get_password == "smshscnn":
        # nextlog = Tk()
        # nextlog.title("Second Window")
        # nextlog.geometry("600x500")
        root.destroy()
        # os.system('object.py')
        os.system('modifiedv5.py')

    
    else:
        messagebox.showerror("Error", "Invalid username or password")


# canva = Canvas(root, width = 600, height = 500)

# Logo
logo = Label(root, text="LOGIN ", font=('Poppins 24'), bg="#181100",fg="white")
logo.place(x=255,y=15)


# Username
username = Entry(root, width=30,bg="white",fg="black",font=('Poppins 16'))
username.grid(row=0,column=1, padx=145,pady=90)

# Password
password = Entry(root, width=30,bg="white",fg="black",font=('Poppins 16'),show="*")
password.grid(row=1,column=1, padx=145)

# Login Button
button = Button(root,text="LOGIN", command=login, width=20,height=2,bg="#3D550C",fg="white")
button.grid(row=2,column=1, padx=10,pady=45)

# Labels
# user = Label(root, text="Username: ", font=('Poppins 15'), bg="#181100",fg="white")
# user.place(x=40,y=60)
user = Label(root,image=update_user, bg="#181100")
user.place(x=90,y=85)
passw = Label(root,image=update_pass, bg="#181100")
passw.place(x=90,y=200)
# passw = Label(root, text="Password: ",font=('Poppins 15'), bg="#181100",fg="white")
# passw.place(x=40,y=148)

# canva.pack()

root.mainloop()

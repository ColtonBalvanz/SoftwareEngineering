import tkinter as tk
from tkinter import *


root = tk.Tk()
root.wm_title("Main") #title of window

root.resizable(width=FALSE,height=FALSE) #Makes the window nonexpandable

myLabel = Label(root,text="My Tool",font="Helvetica 25 bold").pack()
myLabel.place(relx=.2,rely=.1)

def done():
    """Exits the window when 'Exit' button is pressed"""
    root.destroy()

#This block of code is what creates the buttons for each label
modSales = Button(root,text="Modify Sales",width=15,height=2,bg="#c2d6d6")
modSales.place(relx=.17, rely=.18, anchor="c")
viewAudits = Button(root,text="View Audits",width=15,height=2,bg="#c2d6d6")
viewAudits.place(relx=.17, rely=.45, anchor="c")
genDaily = Button(root,text="Generate Daily",width=15,height=2,bg="#c2d6d6")
genDaily.place(relx=.17, rely=.72, anchor="c")
cashMode = Button(root,text="Cashier Mode",width=10,height=5,bg="#c2d6d6")
cashMode.place(relx=.5,rely=.314,anchor="c")
exButton = Button(root,text="Exit",command=done,width=10,height=5,bg="#c2d6d6")
exButton.place(relx=.5,rely=.614,anchor="c")
modData = Button(root,text="Modify Database",width=15,height=2,bg="#c2d6d6")
modData.place(relx=.83,rely=.17,anchor="c")
restock = Button(root,text="View Restock",width=15,height=2,bg="#c2d6d6")
restock.place(relx=.83,rely=.44,anchor="c")
genMonthly = Button(root,text="Generate Monthly",width=15,height=2,bg="#c2d6d6")
genMonthly.place(relx=.83,rely=.71,anchor="c")


root.geometry('{}x{}'.format(750,500))#Size of the window
root.mainloop()

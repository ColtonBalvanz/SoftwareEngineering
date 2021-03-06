import tkinter as tk
from tkinter import *
import os
from myToolPOS import connectTools
#from myToolPOS import *

root = tk.Tk()
root.wm_title("Main") #title of window

root.resizable(width=FALSE,height=FALSE) #Makes the window nonexpandable

#Sets 'My Tool' label at top center of label
myLabel = Label(root,text="My Tool",font="Helvetica 25 bold").pack()
connected = False


def done():
    """Exits the window when 'Exit' button is pressed"""
    root.destroy()

def cashGUI():
    """Opens cashier GUI"""
    os.system("cashierGUI.py")

def generateDailyReport():
    global connected
    if connected == False:
        connected = connectTools.connect()
        connectTools.generateDailyReport()
        connectTools.disconnect()
    else:
        connectTools.generateDailyReport()

def notImplemented():
    """For features that have not yet been implemented"""
    window = tk.Toplevel()
    window.resizable(width=FALSE,height=FALSE)
    label = tk.Label(window,text="This feature has yet to be implemented.",
                     font="Helvetica 10 bold")
    label.pack(side="top",fill="both",padx=10,pady=10)
        
#This block of code is what creates the buttons for each label
modSales = Button(root,text="Modify Sales",width=15,height=2,bg="#c2d6d6",
                  command=notImplemented)
modSales.place(relx=.17, rely=.18, anchor="c")
viewAudits = Button(root,text="View Audits",width=15,height=2,bg="#c2d6d6",
                    command=notImplemented)
viewAudits.place(relx=.17, rely=.45, anchor="c")
genDaily = Button(root,text="Generate Daily",command=generateDailyReport,width=15,height=2,bg="#c2d6d6")
genDaily.place(relx=.17, rely=.72, anchor="c")
cashMode = Button(root,text="Cashier Mode",command=cashGUI,width=10,height=5,bg="#c2d6d6")
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

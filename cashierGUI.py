import tkinter as tk
from tkinter import *

root = tk.Tk()
root.wm_title("Cashier")

root.resizable(width=FALSE,height=FALSE)

canvas = Canvas(root, width = 500, height = 400, bg = 'white')


def done():
    """Exits the window when 'Exit' button is pressed"""
    root.destroy()

exButton = Button(root,text="Exit",command=done,width=18,height=5,bg="red")
exButton.place(relx=.91,rely=.08,anchor="c")
adminView = Button(root,text="Administrative View",width=18,height=5,bg="#c2d6d6")
adminView.place(relx=.91,rely=.25,anchor="c")
voidSale = Button(root,text="Void Sale",width=18,height=5,bg="#c2d6d6")
voidSale.place(relx=.91,rely=.42,anchor="c")
voidItem = Button(root,text="Void Item",width=18,height=5,bg="#c2d6d6")
voidItem.place(relx=.91,rely=.59,anchor="c")
payNow = Button(root,text="Pay Now!",width=18,height=10,bg="#00ff00")
payNow.place(relx=.91,rely=.835,anchor="c")


root.geometry('{}x{}'.format(750,500))
root.mainloop()

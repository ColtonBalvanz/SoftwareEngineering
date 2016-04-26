import tkinter as tk
from tkinter import *

root = tk.Tk()
root.wm_title("Cashier")
from myToolPOS import connectTools

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
text = Text(root, width=14, height=8,font="Helvetica 25 bold")
text.insert('2.0', 'My Tool\n')
text.insert('4.0', "Cashier Mode")
text.tag_configure("center",justify="center")
text.tag_add("center",1.0, "end")
text.place(x=0,y=0)

UPCLabel = Label(root,text="UPC",font="Helvetica 15 bold")
UPCLabel.place(x=1,y=463)
UPCEntry = Entry(root,width=32,bd=3)
UPCEntry.place(x=56,y=470)
<<<<<<< HEAD
totalLabel = Label(root,text="Total:",font="Helvetica 18 bold",relief=GROOVE,
                   width=12,height=5,anchor='nw')
totalLabel.place(x=1,y=310)
totalEntry = Entry(root,width=13)
totalEntry.place(x=189,y=313)
taxLabel = Label(root,text="Sales Tax:",font="Helvetica 18")
taxLabel.place(x=1,y=355)
taxEntry = Entry(root,width=13)
taxEntry.place(x=189,y=360)

#The labels that display the quantity and price of an item
qtyLabel = Label(root,text="Qty #",font="Helvetica 16 bold",relief=RIDGE,
                 width=7)
qtyLabel.place(x=274,y=1)
itemLabel = Label(root,text="Item",font="Helvetica 16 bold",relief=RIDGE,
                  width=11)
itemLabel.place(x=370,y=1)
priceLabel = Label(root,text="Price",font="Helvetica 16 bold",relief=RIDGE,
                   width=7)
priceLabel.place(x=510,y=1)
=======
>>>>>>> origin/master


root.geometry('{}x{}'.format(750,500))
root.mainloop()

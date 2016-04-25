import tkinter as tk
from tkinter import *

root = tk.Tk()
root.wm_title("Cashier")

root.resizable(width=FALSE,height=FALSE)

def done():
    """Exits the window when 'Exit' button is pressed"""
    root.destroy()

exButton = Button(root,text="Exit",command=done,width=12,height=6,bg="red",
                  font="Helvetica 15 bold")
exButton.place(relx=.91,rely=.08,anchor="c")
adminView = Button(root,text="Administrative View",width=12,height=3,bg="#c2d6d6",
                   font="Helvetica 15 bold",wraplength=184, justify=CENTER)
adminView.place(relx=.91,rely=.25,anchor="c")
voidSale = Button(root,text="Void Sale",width=12,height=3,bg="#c2d6d6",
                  font="Helvetica 15 bold")
voidSale.place(relx=.91,rely=.42,anchor="c")
voidItem = Button(root,text="Void Item",width=12,height=3,bg="#c2d6d6",
                  font="Helvetica 15 bold")
voidItem.place(relx=.91,rely=.59,anchor="c")
payNow = Button(root,text="Pay Now!",width=12,height=6,bg="#00ff00",
                font="Helvetica 15 bold")
payNow.place(relx=.91,rely=.835,anchor="c")

text = Text(root, width=15, height=8,font="Helvetica 25 bold")
text.insert('2.0', 'My Tool\n')
#text.insert('4.0', "Cashier Mode")
text.tag_configure("center",justify="center")
text.tag_add("center",1.0, "end")
text.place(x=0,y=0)
cashMode = Label(root,text="Cashier Mode",font="Helvetica 21",bg="white")
cashMode.place(x=45,y=45)


UPCLabel = Label(root,text="UPC",font="Helvetica 15 bold")
UPCLabel.place(x=1,y=463)
UPCEntry = Entry(root,width=32,bd=3)
UPCEntry.place(x=56,y=470)

totalLabel = Label(root,text="Total:",font="Helvetica 18 bold",relief=GROOVE,
                   width=12,height=5,anchor='nw')
totalLabel.place(x=1,y=310)
totalEntry = Entry(root,width=13)
totalEntry.place(x=189,y=313)

taxLabel = Label(root,text="Sales Tax:",font="Helvetica 18")
taxLabel.place(x=1,y=355)
taxEntry = Entry(root,width=13)
taxEntry.place(x=189,y=360)

qtyLabel = Label(root,text="Qty #",font="Helvetica 16 bold",relief=RIDGE,
                 width=7)
qtyLabel.place(x=277,y=1)
itemLabel = Label(root,text="Item",font="Helvetica 16 bold",relief=RIDGE,
                  width=11)
itemLabel.place(x=370,y=1)
priceLabel = Label(root,text="Price",font="Helvetica 16 bold",relief=RIDGE,
                   width=7)
priceLabel.place(x=510,y=1)


root.geometry('{}x{}'.format(750,500))
root.mainloop()

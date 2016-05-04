import tkinter as tk
from tkinter import *
from myToolPOS import *

root = tk.Tk()
root.wm_title("Cashier")

#import myToolPOS

root.resizable(width=FALSE,height=FALSE) #Allows for non-expandable window 

connectTools.connect()

def done():
    """Exits the main window when 'Exit' button is pressed"""
    root.destroy()

def errorChecking():
    """This runs when the user has not inputted a UPC code"""
    window = tk.Toplevel()
    window.resizable(width=FALSE,height=FALSE)
    label = Label(window,text="You must input a UPC code!",font="Helvetica 13 bold")
    label.pack(side="top",fill="both",padx=10,pady=10)
    window.after(4000, lambda: window.destroy())
    window.geometry('{}x{}'.format(280,60))

def paySale():
    connectTools.endSale() 

def implement():
    """For buttons that were not yet implemented"""
    window = tk.Toplevel()
    window.title("Admin View")
    window.resizable(width=FALSE,height=FALSE)
    label = tk.Label(window,text="This feature has yet to be implemented.",
                     font="Helvetica 10 bold")
    label.pack(side="top",fill="both",padx=10,pady=10)

def getUPCNum():
    """Gets UPC number that was inputted by user on the Cashier GUI"""
    #window = tk.Toplevel()
    number = (Entry.get(UPCEntry))
    if len(number) == 0:
        errorChecking()
    else:
        connectTools.newMakeSale(number)
        #might need to eventually put readList here
        readList()

def readList():
    """Places receipt list on cashier GUI"""
    current = ""
    if len(itemList) == 0:
        itemLabel = Label(root, text="                                                                           ",padx=1)
        itemLabel.config(font=("Helvetica",10))
        itemLabel.place(x=279 , y=70)
    else:
        for item in itemList:
            current += str(item) + "\n"
        itemLabel = Label(root, text=current,padx=1)
        itemLabel.config(font=("Helvetica",10))
        itemLabel.place(x=279 , y=70)
       

def removeItem():
    """The window that appears when you click 'Void Item.' This asks for a UPC code to remove."""
    window = tk.Toplevel()
    window.title("Void Item")
    window.resizable(width=FALSE,height=FALSE)
        
    removeLabel = Label(window,text="Enter UPC number to remove:",font="Helvetica 10 bold")
    removeLabel.pack(side="top")

    removeUPC = Entry(window)
    removeUPC.pack(side="top",fill="both",padx=10,pady=10)

    def verifyRemove():
        """This window appears after UPC code has been entered for verification"""
        removeNumber = (Entry.get(removeUPC))
        if len(removeNumber) == 0:
            errorChecking()
        else:
            window=tk.Toplevel()
            window.resizable(width=FALSE,height=FALSE)
            verifyLabel = Label(window,text="Are you sure you want to remove this item?",
                                font="Helvetica 10 bold")
            verifyLabel.pack(side="top",fill="both",padx=10,pady=10)

            def removeCode():
                """Removes an item from their sale list"""
                connectTools.voidItem(removeNumber)
                readList()         
            
            def windowDone():
                """Exits out of the window when user clicks 'NO' after entering UPC code
                   to remove"""
                window.destroy()
                
            #Needs to be placed here so nested functions will properly run   
            yesButton = Button(window,text="YES",width=10,command=removeCode)
            yesButton.place(x=40,y=55)   

            noButton = Button(window,text="NO",width=10,command=windowDone)
            noButton.place(x=190,y=55)
            window.geometry('{}x{}'.format(310,90))
    
    #Needs to be placed here so nested functions will properly run
    UPCButton = Button(window,text="Enter",command=verifyRemove)
    UPCButton.pack(side="bottom")
    window.geometry('{}x{}'.format(290,90))

def removeSale():
    """Window that appears when the user wants to remove a sale"""
    window=tk.Toplevel()
    window.resizable(width=FALSE,height=FALSE)
    verifyLabel = Label(window,text="Are you sure you want to remove this sale?",
                                font="Helvetica 10 bold")
    verifyLabel.pack(side="top",fill="both",padx=10,pady=10)
    
    def deleteSale():
        """Appears after user confirms deletion of sale. New cashier window
           opens"""
        connectTools.voidSale()
        done()
        os.system("cashierGUI.py")

    def windowDone():
        """Exits out of the window when user clicks 'NO' after entering UPC code
        to remove"""
        window.destroy()
        
    #Needs to be placed here so nested functions will properly run
    yesButton = Button(window,text="YES",width=10,command=deleteSale)
    yesButton.place(x=40,y=55)
    noButton = Button(window,text="NO",width=10,command=windowDone)
    noButton.place(x=190,y=55)
    window.geometry('{}x{}'.format(310,90))
    
    
#Buttons that are placed on right hand side of window
exButton = Button(root,text="Exit",command=done,width=12,height=6,bg="red",
                  font="Helvetica 15 bold")
exButton.place(relx=.91,rely=.08,anchor="c")
adminView = Button(root,text="Administrative View",command=implement,width=12,height=3,bg="#c2d6d6",
                   font="Helvetica 15 bold",wraplength=184, justify=CENTER)
adminView.place(relx=.91,rely=.25,anchor="c")
voidSale = Button(root,text="Void Sale",width=12,height=3,bg="#c2d6d6",
                  font="Helvetica 15 bold", command=removeSale)
voidSale.place(relx=.91,rely=.42,anchor="c")
voidItem = Button(root,text="Void Item",command=removeItem,width=12,height=3,bg="#c2d6d6",
                  font="Helvetica 15 bold")
voidItem.place(relx=.91,rely=.59,anchor="c")
payNow = Button(root,text="Pay Now!",command=paySale,width=12,height=6,bg="#00ff00",
                font="Helvetica 15 bold")
payNow.place(relx=.91,rely=.835,anchor="c")

#MyTool label
text = Text(root, width=15, height=8,font="Helvetica 25 bold",background="#c2d6d6")
text.insert('2.0', 'My Tool\n')
text.tag_configure("center",justify="center",background="#c2d6d6")
text.tag_add("center",1.0, "end")
text.place(x=0,y=0)

#Label under 'My Tool'
cashMode = Label(root,text="Cashier Mode",font="Helvetica 21",bg="#c2d6d6")
cashMode.place(x=45,y=45)

#Labels and entries that correspond to the total price, sales tax,
#and UPC code
UPCLabel = Label(root,text="UPC",font="Helvetica 15 bold")
UPCLabel.place(x=1,y=463)
UPCEntry = Entry(root,width=20,bd=3)
UPCEntry.place(x=55,y=468)
totalLabel = Label(root,text="Total:",font="Helvetica 18 bold",relief=GROOVE,
                   width=12,height=5,anchor='nw')
totalLabel.place(x=1,y=310)
#totalEntry = Entry(root,width=13)
#totalEntry.place(x=189,y=313)
taxLabel = Label(root,text="Sales Tax:",font="Helvetica 18")
taxLabel.place(x=1,y=355)
#taxEntry = Entry(root,width=13)
#taxEntry.place(x=189,y=360)
#clickPayNow = Label(root,text="Click\n Pay Now!",font="Helvetica 12")
#clickPayNow.place(x=192,y=380)

#The labels that display the quantity and price of an item
qtyLabel = Label(root,text="UPC",font="Helvetica 16 bold",relief=RIDGE,
                 width=7)
qtyLabel.place(x=274,y=1)
itemLabel = Label(root,text="Item",font="Helvetica 16 bold",relief=RIDGE,
                  width=11)
itemLabel.place(x=370,y=1)
priceLabel = Label(root,text="Price",font="Helvetica 16 bold",relief=RIDGE,
                   width=7)
priceLabel.place(x=510,y=1)

#For UPC entry
UPCButton = Button(root,text="Enter",command=getUPCNum,width=8,height=2,bg="#00ff00",
                  font="Helvetica 10 bold")
UPCButton.place(relx=.31,rely=.95,anchor="c")



root.geometry('{}x{}'.format(750,500)) #Size of window
root.mainloop()

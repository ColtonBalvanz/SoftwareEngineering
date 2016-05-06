from tkinter import *
#from tkMessageBox import *
itemList = list()

def newMakeSale(itemID):
    item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
    if item != None:
        return tuple(itemID, item[11], item[9])
    else:
        return tuple(None, None, None)

def voidItem(itemID):
    global itemList
    item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
    if item != None:
        listItem = tuple([itemID, item[11], item[9]])
        if listItem in itemList:
            itemList.remove(listItem)
        else:
            showerror("Error", "UPC code not found in cart")
            

def voidSale():
    global itemList
    itemList = list()

def endSale():
    #used when the button "Pay Now!" is clicked
    global itemList
    global ticketID
    global itemNames
    global itemIDs
    global itemPrices

    for item in itemList:
        itemIDs.append(item[0])
        itemNames.append(item[1]
        itemPrices.append(item[2])
    sale = list([int(ticketID), itemIDs, itemPrices])
    if not connectTools.add_sale(sale)==True:
        window = tk.Toplevel()
        window.resizable(width=FALSE,height=FALSE)
        label = Label(window,text="The system was unable to submit the sale to the sales database. \
\nPlease contact IT for more information.",font="Helvetica 13 bold")
        label.pack(side="top",fill="both",padx=10,pady=10)
        window.after(3000, lambda: window.destroy())
        window.geometry('{}x{}'.format(480,60))
    for itemID in itemIDs:
        connectTools.decrement(1, itemID)
    window = tk.Toplevel()
    window.resizable(width=FALSE,height=FALSE)
    label = Label(window,text="Sale completed!",font="Helvetica 13 bold")
    label.pack(side="top",fill="both",padx=10,pady=10)
    window.after(3000, lambda: window.destroy())
    window.geometry('{}x{}'.format(480,60))

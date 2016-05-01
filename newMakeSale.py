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
    

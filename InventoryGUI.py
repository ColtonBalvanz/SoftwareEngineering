import tkinter as tk
from tkinter import *
from tkinter import ttk
from myToolPOS import connectTools

inventory = None
table_data = None


def createWindow():
    global inventory
    if connectTools.connect() == True:
        print("Successfully connected to the database!")
        table_data = connectTools.query("inventory", "*")
        ##print(table_data)
        connectTools.disconnect()
    else:
        print("Connection was a failure!")
    columns = ("item_id", "quantity", "category", "price", "cost",
                            "desired_quantity", "sale", "sale_start", "sale_end",
                            "sale_price" , "supplier")
    proper_columns = ("Item ID", "Quantity", "Category", "Price", "Cost",
                      "Desired Quantity", "Sale?", "Sale Start Date", "Sale End Date",
                      "Sale Price", "Supplier")
    proper_widths = (85, 55, 80, 60, 60, 100, 40, 100, 100, 60, 80)
    
    root = tk.Tk()
    root.wm_title("Modify Inventory")
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('{}x{}'.format(950,600))#Size of the window
    inventory = ttk.Treeview(root, columns=(columns), show="headings")
    ##inventory.Scrollable = True;
    inventory["columns"] = columns
    for headings in range(0,len(proper_columns)):
        inventory.heading(headings, text=proper_columns[headings])
        inventory.column(columns[headings], width=proper_widths[headings])
    for row in range(0, len(table_data)):
        inventory.insert("", row, values=table_data[row])
    ##inventory.insert("","end", values = ())
    inventory.grid()
    inventory.bind('<ButtonRelease-1>', selectItem)
    ##root.grid(10, 10, 5, 5)
    root.mainloop()

def selectItem(a):
    global inventory
    curItem = inventory.focus()
    print(inventory.item(curItem))

def close():
    root.destroy()

##def modifyrow():
createWindow()

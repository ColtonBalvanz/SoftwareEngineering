import tkinter as tk
from tkinter import *
from tkinter import ttk
from myToolPOS import connectTools
from psycopg2.extensions import AsIs

inventory = None
table_data = None
main = None
root = None
button_panel = None
connected = False

def close():
    global root
    connectTools.disconnect()
    root.destroy()

def refresh():
    global connected
    if connected == True:
        table_data = connectTools.query("inventory", "*")
    else:
        connected = connectTools.connect()
        table_data = connectTools.query("inventory", "*")

def createWindow():
    global inventory
    global root
    global main
    global button_panel
    global table_data
    global connected
    if connected == True:
        table_data = connectTools.query("inventory", "*")
    else:
        connected = connectTools.connect()
        table_data = connectTools.query("inventory", "*")
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
    main = tk.Frame(root)
    main.grid(sticky="nesw")
    main.columnconfigure(0,weight=1)
    main.rowconfigure(0,weight=1)
    button_panel = tk.Frame(root)
    button_panel.grid(row=0, column=1)
    inventory = ttk.Treeview(main, columns=(columns), show="headings")
    inventory["columns"] = columns
    for headings in range(0,len(proper_columns)):
        inventory.heading(headings, text=proper_columns[headings])
        inventory.column(columns[headings], width=proper_widths[headings])
    for row in range(0, len(table_data)):
        inventory.insert("", row, values=table_data[row])
    ##xsb = ttk.Scrollbar(inventory, orient='horizontal', command=inventory.xview)
    ##xsb.grid(row=1, column=1, sticky='ew')
    inventory.grid(row=0, column=0, sticky='ns')
    ##ysb = ttk.Scrollbar(inventory, orient='vertical', command=inventory.yview)
    add = tk.Button(button_panel, text="Add", command=addItem, width=17, height=10)
    add.grid(row=0, column=0, columnspan=1, rowspan=1)
    modify = tk.Button(button_panel, text="Modify", command=modifyItem, width=17, height=10)
    modify.grid(row=1, column=0, columnspan=1, rowspan=1)
    close = tk.Button(button_panel, text="Exit", command=root.destroy, width=17, height=10)
    close.grid(row=2, column=0, columnspan=1, rowspan=1)
    ##inventory.bind('<ButtonRelease-1>', selectItem)
    ##root.grid(10, 10, 5, 5)
    root.mainloop()

def modifyItem():
    global inventory
    curItem = inventory.focus()
    print(inventory.item(curItem))
    window = tk.Toplevel()
    window.title("Modify Item")
    window.resizable(width=FALSE, height=FALSE)
    modifyLabel = Label(window, text="What would you like to change?")
    modifyLabel.pack(side="top")
    otherLabel= Label(window, text=inventory.item(curItem).get('values'))
    otherLabel.pack()

def addItem():

    COLUMN_LABELS = ["Item ID", "Quantity", "Category", "Price", "Cost",
                      "Desired Quantity", "Sale?", "Sale Start Date", "Sale End Date",
                      "Sale Price", "Supplier", "Item Name"]

    def add():
        stuff = list()
        count = 0
        for column in COLUMN_LABELS:
            if count==0 or count==1 or count==3 or count==4 or count==5:
                stuff.append(int(entry[column].get()))
            elif count==6:
                if entry[column].get()=="False":
                    stuff.append(False)
                elif entry[column].get()=="True":
                    stuff.append(True)
                else:
                    print("You goof!")
            elif entry[column].get()=="":
                stuff.append(None)
            else:
                stuff.append(entry[column].get())
            count+=1
        print(stuff)
        if connectTools.add_item(stuff)==True:
            window = tk.Toplevel()
            window.title("Successful!")
            window.resizable(width=FALSE, height=FALSE)
            text = Label(window, text="The add was successful!")
            text.pack()
        else:
            window = tk.Toplevel()
            window.title("Unsuccessful!")
            window.resizable(width=FALSE, height=FALSE)
            text = Label(window, text="The add was unsuccessful!")
            text.pack()
            
            
    
    entry = {}
    label = {}
    window = tk.Toplevel()
    window.title("Add item")
    window.resizable(width=FALSE, height=FALSE)
    window.grid()
    i = 0
    for column in COLUMN_LABELS:
        labels = Label(window, text=column)
        labels.grid(row=0, column=i)
        label[column] = labels
        
        entries = Entry(window, width=15)
        entries.grid(row=1, column=i)
        entry[column] = entries
        i += 1
    blank = Label(window, text="")
    blank.grid(row=0, column=len(COLUMN_LABELS))
    submit = Button(window, text="Submit", command=add)
    submit.grid(row=1, column=len(COLUMN_LABELS))


createWindow()

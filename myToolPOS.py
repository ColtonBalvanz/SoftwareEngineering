import sys
import pprint
import psycopg2
from psycopg2.extensions import AsIs
import urllib.parse
import time
import xlwt
##from tkinter import Tk, Frame, Button, BOTH, Label
##import time
##This is the new version!!!

## class GUI
##      global upccode


counter = 0
dateString = str(time.strftime("%Y%m%d"))
BOLD_CELLS = xlwt.easyxf('font: bold on')
DATE_CELL = xlwt.easyxf(num_format_str='MM-DD-YYYY')
GENERATE_WORTH_NAME = "Worth_report_" + str(time.strftime("%m-%d-%Y"))


##Try not to get too excited about this. I copied and pasted from the
##GUI program I was working with to try out tkinter. :p Hopefully here
##is where we link up the buttons. Clock works, quit should still work.
##
##class GUI(Frame):
##  
##    def __init__(self, parent):
##        Frame.__init__(self, parent, background="grey")   
##        self.parent = parent
##        self.initUI()
##        self.update_clock()
##
##    def update_clock(self):
##        current = time.strftime("%I:%M:%S%p %B %d, %Y")
##        someClock = Label(self, text=current, font=(10), padx=50)
##        someClock.place(x=0, y=80)
##        self.after(1000, self.update_clock)
##
##    def quit():
##        global root
##        root.quit()
##        
##    
##    def initUI(self):
##      
##        self.parent.title("My Tool Client")
##        self.pack(fill=BOTH, expand=1)
##        quitButton = Button(self, text="Exit",
##            command=quit, padx=50, pady=30)
##        quitButton.place(x=674, y=0)
##        adminButton = Button(self, text="Void Item(s)", padx=28, pady=30)
##        adminButton.place(x=674, y=84)
##        myToolLabel = Label(self, text="Welcome to MyTool!", font=("-weight bold", 24), padx=20)
##        employeeName = Label(self, text="Bob", padx=119)
##        myToolLabel.place(x=0, y=0)
##        employeeName.place(x=0, y=42)



class connectTools:
##These are some of the variables that will be reused often throughout
##this class. conn is our variable for the connection called by many of
##the methods in this class. server_info is a string of the server
##information stored in a text file outside of our code. The url is the
##parsed version of the string to work with establishing the connection.
##The cursor is a tool that will make modifications to the tables in our
##database.

    conn = None
    server_info = None
    url = None
    cursor = None

    
    def connect():
##The connect method opens the initial connection to the server. To
##close the connection, call disconnect() after calling connect(). The
##connection will stay open to call other methods defined in this class.
        
        try:
            global server_info
            server_info = open('server_info.txt', 'r')
            global url
            url = urllib.parse.urlparse(server_info.read())
            urllib.parse.uses_netloc.append("postgres")
            global conn
            conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
            global cursor
            cursor = conn.cursor()
            return True
        except:
            return False

    def disconnect():
##This is called after connect(), and it should not be called before
##connect().

        try:
            global conn
            conn.close()
        except:
            print("Sorry, I am not even connected right now. :o")

    def query(table, column):
##This method allows the user to query which table to access and which
##column in the table. It may be useful, but query_single is more
##useful. It has the ability to display the whole contents of the table
##at half the expense of query_single.

        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s""", {"table": AsIs(table), "column": AsIs(column)})
        return cursor.fetchall()

    def query_single(table, column, args):
##This is helpful for when we want to look up an item more specifically.
##We can look up the price from a barcode and other related columns
##prior to making a sale.
        
        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s WHERE %(args)s;""", {"table": AsIs(table), "column": AsIs(column), "args": AsIs(args)})
        return cursor.fetchone()

    def query_column_names(table):
        global cursor
        cursor.execute("SELECT * FROM  information_schema.tables WHERE table_schema = 'schema_name' AND table_name = 'inventory'")
        print(cursor.fetchall())

    def modify_single(table, operation, location):
##modify_single will do the work of subtracting a number of items from a
##purchase, plus any updates we might have on updating a specific item,
##such as updating a price or setting the sale of an item.
        
        global conn
        global cursor
        try:
            cursor.execute("""UPDATE ONLY %(table)s SET %(operation)s WHERE %(location)s;""", {"table": AsIs(table), "location": AsIs(location), "operation": AsIs(operation)})
            conn.commit()
            return True
        except:
            print("Sorry, I was unable to modify with that statement")
            return False
            
    def add_sale(row):
##add_sale has the responsibility to add a row in the sales table, and
##list items associated with that sale.
        
        global conn
        global cursor
        try:
            cursor.execute(
                """INSERT INTO sales (sale_id, items_purchased, item_prices)
    VALUES (%s, %s, %s);""", row)
            conn.commit()
            return True
        except:
            print("Sorry, that was not a valid entry")
            return False

    def increment(add):
        sqlstring = "quantity = quantity + " + add
        return sqlstring
        

    def add_item(table, row):
##add_item will add a new item to the inventory database. It will add
##whatever new item My Tool chooses to carry in the store. It takes the
##arguement of the table name and the values of that new row, which are
##the item_id, the quantity, category of the item, price, cost, how many
##to keep in stock regularly, whether the item is on sale or not, the
##sale start and end dates, the sale price, and who supplies that item.

        global conn
        global cursor
        try:
            cursor.execute(
            """INSERT INTO inventory (item_id, quantity, category, price, cost, desired_quantity, sale, sale_start, sale_end, sale_price, supplier)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", row)
            conn.commit()
            return True
        except:
            print("Sorry, I could not add this item")
            return False

    def makeSale():
##The makeSale() method is responsible for producing the sale of a
##customer. It will also print out a physical receipt the customer can
##take with them.
        global counter
        global dateString
        counter += 1
        ticketID = dateString + str(counter)
        receiptString = ""
        while True:
            inputID = input("Scan item or input item ID. Hit enter with no item ID to end sale. " )
            if inputID == "":
                break
            else:
                item = connectTools.query_single("inventory", "*", "item_id = " + inputID)
                if item != None:
                    itemName = item[11]
                    itemPrice = item[3]
                    print(itemName, itemPrice)
            ##
            #retrieve item name and price
            #add to receiptString
    #submit to sales db
    ##connectTools.add_sale()
    #decrement inventory
        print(ticketID)
        print("Thanks for shopping at My Tool!")
        print("Have a great day!")
        print(receiptString)

    def decrement(subtract):
##decrement() changes the quantity of an item in a database. There is
##not much important about this yet.
        sqlstring = "quantity = quantity - " + subtract
        return AsIs(sqlstring)
    def increment(add):
##increment() changes the quanity of an item in a database.
        sqlstring = "quantity = quantity + " + add
        return AsIs(sqlstring)


##class loginAccess:

##    def login(user_name, password):


def main():
##This probably won't be here for too long. Once we have a GUI we will
##have a more functional main() to operate out sale system.

    
    location = "item_id = 12000151200"
    operation = connectTools.increment('5')
    column_name = "*"
    table_name = "inventory"
    list1 = (12000151200, 10, 'beverage', 189, 150, 5, None, None, None, None, 'MY TOOL INC')
    
    if connectTools.connect()==True:
        print("The connection was a success!")
##        print(connectTools.query(table_name, column_name))
        connectTools.makeSale()
        connectTools.query_column_names("inventory")
        connectTools.disconnect()
    else:
        print("Whoops! I can't even!")
        exit()
##    time = makeSale.generate_id()
##This works, I don't know how, but it does.
if __name__ == '__main__':
    main()

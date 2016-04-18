import sys
import pprint
import psycopg2
from psycopg2.extensions import AsIs
import urllib.parse
import time


## class GUI
##      global upccode


counter = 0
dateString = str(time.strftime("%Y%m%d"))

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
        except:
            print("Sorry, I am unable to connect to the database")

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
        records = cursor.fetchall()
        pprint.pprint(records)

    def query_single(table, column, args):
##This is helpful for when we want to look up an item more specifically.
##We can look up the price from a barcode and other related columns
##prior to making a sale.
        
        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s WHERE %(args)s;""", {"table": AsIs(table), "column": AsIs(column), "args": AsIs(args)})
        return cursor.fetchone()

    def modify_single(table, operation, location):
##modify_single will do the work of subtracting a number of items from a
##purchase, plus any updates we might have on updating a specific item,
##such as updating a price or setting the sale of an item.
        
        global conn
        global cursor
        try:
            cursor.execute("""UPDATE ONLY %(table)s SET %(operation)s WHERE %(location)s;""", {"table": AsIs(table), "location": AsIs(location), "operation": AsIs(operation)})
            conn.commit()
        except:
            print("Sorry, I was unable to modify with that statement")
            
            
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
        except:
            print("Sorry, that was not a valid entry")

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
        except:
            print("Sorry, I could not add this item")

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
            inputID = input("Scan item or input item ID. Hit enter with no item ID to end sale. ")
            if inputID == "":
                break
            else:
                item = connectTools.query_single("inventory", "*", "item_id = " + inputID)
                if item != None:
                    itemName = item[11]
                    price = item[3]
                    print(itemName, price)

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
    connectTools.connect()
    connectTools.modify_single(table_name, operation, location)
##    connectTools.query(table_name, column_name)   
##    connectTools.query_single(table_name, column_name, arguing)
##    connectTools.add_item(list1)
    connectTools.makeSale()
    connectTools.disconnect()
##    time = makeSale.generate_id()
##    connectTools.makeSale()

##This works, I don't know how, but it does.
if __name__ == '__main__':
    main()

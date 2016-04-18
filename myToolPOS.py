import sys
import pprint
import psycopg2
from psycopg2.extensions import AsIs
import urllib.parse
import time


## class GUI
##      global upccode



class connectTools:
    conn = None
    server_info = None
    url = None
    cursor = None

    
    def connect():
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
        global conn
        conn.close()

    def query(table, column):

        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s""", {"table": AsIs(table), "column": AsIs(column)})
        records = cursor.fetchall()
        pprint.pprint(records)

    def query_single(table, column, args):
        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s WHERE %(args)s;""", {"table": AsIs(table), "column": AsIs(column), "args": AsIs(args)})
        records = cursor.fetchall()
        pprint.pprint(records)

    def modify_single(table, operation, location):
        global conn
        global cursor
        try:
            cursor.execute("""UPDATE ONLY %(table)s SET %(operation)s WHERE %(location)s;""", {"table": AsIs(table), "location": AsIs(location), "operation": AsIs(operation)})
            conn.commit()
        except:
            print("Sorry, I was unable to modify with that statement")
            
            
    def add_sale(row):
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

        global conn
        global cursor
        try:
            cursor.execute(
            """INSERT INTO inventory (item_id, quantity, category, price, cost, desired_quantity, sale, sale_start, sale_end, sale_price, supplier)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", row)
            conn.commit()
        except:
            print("Sorry, I could not add this item")

class saleOperations

    counter = 0
    dateString = str(time.strftime("%Y%m%d"))

    def makeSale():
        global counter
        counter += 1
        ticketID = dateString + str(counter)
        receiptString = ""
        while True:
            inputID = input("Scan item or input item ID. Hit enter with no item ID to end sale." )
            if inputID == "":
                break
            else:
                pass
            #connect to the database
            #check item exists
            #retrieve item name and price
            #add to receiptString
    #submit to sales db
    #decrement inventory
        print(ticketID)
        print("Thanks for shopping at My Tool!")
        print("Have a great day!")
        print(receiptString)

    def decrement(subtract):
        sqlstring = "quantity = quantity - " + subtract
        return sqlstring

def main():
    location = "supplier = 'MY TOOL INC'"
    operation = saleOperations.decrement(5)
    column_name = "*"
    table_name = "inventory"
    list1 = (12000151200, 10, 'beverage', 189, 150, 5, None, None, None, None, 'MY TOOL INC')
    connectTools.connect()
    connectTools.modify_single(table_name, operation, location)
##    connectTools.query(table_name, column_name)   
##    connectTools.query_single(table_name, column_name, arguing)
##    connectTools.add_item(list1)
    connectTools.disconnect()
    time = makeSale.generate_id()
if __name__ == '__main__':
    main()

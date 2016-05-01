import tkinter as tk
import sys
import pprint
import psycopg2
from psycopg2.extensions import AsIs
import urllib.parse
import time
import xlwt
from datetime import datetime
from tkinter import *
import os


counter = 1
BRAND_CELL = xlwt.easyxf("font: bold on; align: horiz center, vert centre;")
DATE_CELL = xlwt.easyxf(num_format_str='MM-DD-YYYY')
GENERATE_WORTH_NAME = "Worth_Report_" + str(time.strftime("%m-%d-%Y"))
GENERATE_DAILY_REPORT_NAME = "Daily_Operations_Report" +str(time.strftime("%m-%d-%Y"))
ALIGN_RIGHT = xlwt.easyxf("align: horiz right")
ALIGN_CENTER = xlwt.easyxf("align: horiz center")
BOLDED_CENTER = xlwt.easyxf("align: horiz center; font: bold on")
MONEY_FORMAT = xlwt.easyxf(num_format_str = '$#,##0.00')
REMOVE_SCIENTIFIC = xlwt.easyxf(num_format_str = '0')
itemList = list()


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
    dateString = None
    ticketID = None
    itemNames = list()
    itemPrices = list()
    subTotal = 0
    salesTax = 0
    inputIDlist = list()
   # itemList = list()
    
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
            connectTools.check_count()
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
            print("Sorry, I am not even connected right now.")
            
    def check_count():
        global cursor
        cursor.execute("""SELECT MAX(sale_id) FROM sales;""")
        current = cursor.fetchone()
        if current != None:
            global ticketID
            global dateString
            global counter
            dateString = str(time.strftime("%Y%m%d"))
            #ticketID = dateString + str(counter)
            ticketID = dateString + "000"
            ticketID = int(ticketID) + counter
            if int(ticketID) <= int(current[0]):
                print("Adjusting the counter...")
                counter+=1
    ##              print(ticketID)
                connectTools.check_count()
            else:
                print("Counter is now in sync!")
    ##              print(ticketID)
        else:
            print("Counter looks good already!")

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
        

    def add_item(row):
##add_item will add a new item to the inventory database. It will add
##whatever new item My Tool chooses to carry in the store. It takes the
##arguement of the values of that new row, which are the item_id, the
##quantity, category of the item, price, cost, how many to keep in stock
##regularly, whether the item is on sale or not, the sale start and end
##dates, the sale price, and who supplies that item.

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
        global itemNames
        global itemPrices
        global inputIDlist
        global grandTotal
        global salesTax
        global subTotal
        counter += 1
        receiptString = ""
        itemNames = list()
        itemPrices = list()
        subTotal = 0
        salesTax = 0
        inputIDlist = list()
        while True:
            inputID = input("Scan item or input item ID. Hit enter with no item ID to end sale. ")
            if inputID == "":
                break
            else:
                item = connectTools.query_single("inventory", "*", "item_id = " + inputID)
                if item != None:
                    inputIDlist.append(inputID)
                    itemNames.append(item[11])
                    if item[6] == True:
                        global grandTotal
                        itemPrices.append(item[9])
                        subTotal += item[9]
                    else:
                        global grandTotal
                        itemPrices.append(item[3])
                        subTotal+= item[3]
                else:
                    print("Item was not found.")
            salesTax = round((subTotal*7)/100)
        sale = list([int(ticketID), inputIDlist, itemPrices])
        if connectTools.add_sale(sale)==True:
            print("I added the sale!")
        else:
            print("Sorry, I could not add this item")
        for itemID in inputIDlist:
            connectTools.decrement(1, itemID)
        print(ticketID)
        print(itemNames)
        print(itemPrices)
        print("Sub total: " + str(subTotal))
        print("Sales tax: " + str(salesTax))
        connectTools.generateReceipt(itemNames, itemPrices, subTotal, salesTax)

    def newMakeSale(itemID):
        global itemList
        item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
        if item != None:
            itemList.append(tuple([itemID, item[11], item[9]]))
        else:
            window = tk.Toplevel()
            window.resizable(width=FALSE,height=FALSE)
            label = Label(window,text="The UPC code you entered was not found in the database!",font="Helvetica 13 bold")
            label.pack(side="top",fill="both",padx=10,pady=10)
            window.after(3000, lambda: window.destroy())
            window.geometry('{}x{}'.format(480,60))

    def voidItem(itemID):
        global itemList
        item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
        if item != None:
            listItem = tuple([itemID, item[11], item[9]])
            if listItem in itemList:
                itemList.remove(listItem)
        else:
            window = tk.Toplevel()
            window.resizable(width=FALSE,height=FALSE)
            label = Label(window,text="The UPC code you entered was not found in the cart!",font="Helvetica 13 bold")
            label.pack(side="top",fill="both",padx=10,pady=10)
            window.after(3000, lambda: window.destroy())
            window.geometry('{}x{}'.format(450,60))
            
    def voidSale():
        global itemList
        itemList = list()


    def generateReceipt(itemNames, itemPrices, subTotal, salesTax):
##This new method relies on being called from makeSale(). It takes two
##lists, and two integer values to generate a receipt for the customer.
##It prints out to an excel file with formatted numbers. This is the
##best we have to make a receipt for the cashier. It launches the file
##after it has been created so the customer can print the receipt.
        
        global ticketID
        global ALIGN_RIGHT
        global ALIGN_CENTER
        receipt = xlwt.Workbook()
        sale = receipt.add_sheet('Customer Receipt')
        sale.write_merge(0, 1, 0, 5, "My Tool", BRAND_CELL)
        sale.write_merge(2, 2, 0, 3, "Today's date:", xlwt.easyxf('align: horiz right'))
        sale.write_merge(2, 2, 4, 5, str(time.strftime("%m-%d-%Y")), xlwt.easyxf('align: horiz right'))
        sale.write_merge(3, 3, 0, 3, "Your unique sale ID:", xlwt.easyxf('align: horiz right'))
        sale.write_merge(3, 3, 4, 5, ticketID, xlwt.easyxf('align: horiz right'))
        sale.write_merge(4, 4, 0, 3, "Item", BRAND_CELL)
        sale.write_merge(4, 4, 4, 5, "Price", BRAND_CELL)
        for x in range(0, len(itemNames)):
            sale.write_merge(5+x, 5+x, 0, 3, itemNames[x])
            sale.write_merge(5+x, 5+x, 4, 5, str(itemPrices[x]/100), ALIGN_RIGHT)
        sale.write_merge(5+len(itemNames), 5+len(itemNames), 0, 3, "Sales Tax:", ALIGN_RIGHT)
        sale.write_merge(5+len(itemNames), 5+len(itemNames), 4, 5, str(salesTax/100), ALIGN_RIGHT)
        sale.write_merge(6+len(itemNames), 6+len(itemNames), 0, 3, "Sub total:", ALIGN_RIGHT)
        sale.write_merge(6+len(itemNames), 6+len(itemNames), 4, 5, str(subTotal/100), ALIGN_RIGHT)
        sale.write_merge(7+len(itemNames), 7+len(itemNames), 0, 3, "Total:", ALIGN_RIGHT)
        sale.write_merge(7+len(itemNames), 7+len(itemNames), 4, 5, str((salesTax+subTotal)/100), ALIGN_RIGHT)
        sale.write_merge(8+len(itemNames), 8+len(itemNames), 0, 5, "Thanks for shopping at My Tool!", ALIGN_RIGHT)
        sale.write_merge(9+len(itemNames), 9+len(itemNames), 0, 5, "Have a great day!", ALIGN_CENTER)
        receipt.save('Customer_receipt_' + ticketID+'.xls')
        os.system("start Customer_receipt_" + ticketID+ '.xls')

    def generateWorth():
        global GENERATE_WORTH_NAME
        global DATE_CELL
        global MONEY_FORMAT
        global ALIGN_CENTER
        rowIndex = 3
        records = connectTools.query('inventory', '*')

        COLUMN_HEADINGS = [("Item ID"), ("Item Name"),
                           ("Quantity"), ("Cost"), ("Total Cost")]
        report = xlwt.Workbook()
        dailyWorth = report.add_sheet(GENERATE_WORTH_NAME)
        dailyWorth.write_merge(0, 1, 0, 4, GENERATE_WORTH_NAME, BRAND_CELL)
        for x in range(0, len(COLUMN_HEADINGS)):
            dailyWorth.write(2,x, COLUMN_HEADINGS[x], BOLDED_CENTER)
        
        for row in records:
            itemID = row[0]
            itemName = row[11]
            quantity = row[1]
            cost = row [4]
            totalCost = cost*quantity
            dailyWorth.write(rowIndex, 0, itemID, REMOVE_SCIENTIFIC)
            dailyWorth.write(rowIndex, 1, itemName, ALIGN_CENTER)
            dailyWorth.write(rowIndex, 2, quantity)
            dailyWorth.write(rowIndex, 3, (cost/100), MONEY_FORMAT)
            dailyWorth.write(rowIndex, 4, (totalCost/100), MONEY_FORMAT)
            rowIndex += 1
        for col in range(0, len(COLUMN_HEADINGS)):
            column = dailyWorth.col(col)
            column.width = 256*25
        report.save(GENERATE_WORTH_NAME + '.xls')
        os.system("start " + GENERATE_WORTH_NAME + '.xls')

    def generateDailyReport():
        global GENERATE_DAILY_REPORT_NAME
        global DATE_CELL
        records = connectTools.query('sales', '*')
            
        COLUMN_HEADINGS = [("Sales Today"), ("Sales Yesterday"),
                           ("Profit Today"), ("Profit Yesterday")]
        report = xlwt.Workbook()
        dailyOperations = report.add_sheet(GENERATE_DAILY_REPORT_NAME)
        dailyOperations.write_merge(0, 1, 0, 4, GENERATE_DAILY_REPORT_NAME,
                                    BRAND_CELL)
        for x in range(0, len(COLUMN_HEADINGS)):
            dailyOperations.write(2,x, COLUMN_HEADINGS[x], BOLDED_CENTER)

        report.save(GENERATE_DAILY_REPORT_NAME+ '.xls')
        os.system("start " + GENERATE_DAILY_REPORT_NAME + '.xls')
        

    def parse_list(alist):
        newList = list()
        item_ids = list()
        item_prices = list()
        sale_ids = list()
        newList.append(sale_ids)
        newList.append(item_ids)
        newList.append(item_prices)
        #print(newList)
        individual_item = ""
        for row in range(0,len(alist)):
            print(row)
            newList[0].append(alist[row][0])
            #print(newList[0])
            for index in range(1,3):
                individual_item = ""
                for character in alist[row][index]:
                    #if alist[row][index][character] == ',':
                    if character == ',':
                        newList[index].append(individual_item)
                        individual_item = ""
                        #print(newList)
                    #elif alist[row][index][character] == '{':
                    elif character == '{':
                        #print("Begin list")
                        pass
                    #elif alist[row][index][character] == '}':
                    elif character == '}':
                        newList[index].append(individual_item)
                        #individual_item = ""
                        #print("End list")
                        pass
                    #elif alist[row][index][character] == ' ':
                    elif character == ' ':
                        #print("A space")
                        pass
                    else:
                        individual_item += character
                        #print(individual_item)
        return newList    
    

    def decrement(subtract, itemID):
##decrement() changes the quantity of an item in a database. There is
##not much important about this yet.
        sqlstring = "quantity = quantity - " + str(subtract)
        global conn
        global cursor
        try:
            cursor.execute("""UPDATE ONLY inventory SET quantity =
            quantity - %(subtract)s WHERE item_id = %(item_id)s;""",
            {"item_id": AsIs(itemID) , "subtract":
            AsIs(subtract)})
            conn.commit()
            return True
        except:
            print("Sorry, I was unable to modify with that statement")
            return False
    
    def increment(add, itemID):
##increment() changes the quanity of an item in a database. We can use this
## to do returns on items.
        sqlstring = "quantity = quantity + " + str(add)
        global conn
        global cursor
        try:
            cursor.execute("""UPDATE ONLY inventory SET quantity =
            quantity - %(add)s WHERE item_id = %(item_id)s;""",
            {"item_id": AsIs(itemID) , "add":
            AsIs(add)})
            conn.commit()
            return True
        except:
            print("Sorry, I was unable to modify with that statement")
            return False



def main():
##This probably won't be here for too long. Once we have a GUI we will
##have a more functional main() to operate out sale system.

    if connectTools.connect()==True:
        print("The connection was a success!")
        #connectTools.makeSale()
        connectTools.generateWorth()
        connectTools.disconnect()
    else:
        print("Whoops! I can't connect!")
        exit()
##This works, I don't know how, but it does.
if __name__ == '__main__':
    main()

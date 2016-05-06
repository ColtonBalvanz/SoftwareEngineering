import tkinter as tk
import sys
import pprint
import psycopg2
from psycopg2.extensions import AsIs
from datetime import timedelta
import urllib.parse
import time
import xlwt
from datetime import datetime
from datetime import date
from tkinter import *
import os


counter = 1
BRAND_CELL = xlwt.easyxf("font: bold on; align: horiz center, vert centre;")
DATE_CELL = xlwt.easyxf(num_format_str='MM-DD-YYYY')
GENERATE_WORTH_NAME = "Worth_Report_" + str(time.strftime("%m-%d-%Y"))
GENERATE_DAILY_REPORT_NAME = "Daily_Operations_Report_" + str(time.strftime("%m-%d-%Y"))
ALIGN_RIGHT = xlwt.easyxf("align: horiz right")
ALIGN_CENTER = xlwt.easyxf("align: horiz center")
BOLDED_CENTER = xlwt.easyxf("align: horiz center; font: bold on")
MONEY_FORMAT = xlwt.easyxf(num_format_str = '$#,##0.00')
REMOVE_SCIENTIFIC = xlwt.easyxf(num_format_str = '0')
itemList = list()


class connectTools:
    """These are some of the variables that will be reused often throughout
       this class. conn is our variable for the connection called by many of
       the methods in this class. server_info is a string of the server
       information stored in a text file outside of our code. The url is the
       parsed version of the string to work with establishing the connection.
       The cursor is a tool that will make modifications to the tables in our
       database."""

    global itemList
    global ticketID
    global itemNames
    global itemIDs
    global itemPrices
    global subtotal
    global salesTax
    subtotal = 0
    salesTax = 0
    conn = None
    server_info = None
    url = None
    cursor = None
    dateString = None
    ticketID = None
    itemNames = list()
    itemPrices = list()
    inputIDlist = list()
    itemIDs = list()

    
    def connect():
        """The connect method opens the initial connection to the server. To
           close the connection, call disconnect() after calling connect(). The
           connection will stay open to call other methods defined in this class."""
        
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
        """This is called after connect(), and it should not be called before
           connect()."""
        try:
            global conn
            conn.close()
        except:
            print("Sorry, I am not even connected right now.")

            
    def check_count():
        """Checks if it can overwrite the current sale ID so a new sale can
           take place"""

        global cursor
        cursor.execute("""SELECT MAX(sale_id) FROM sales;""")
        current = cursor.fetchone()
        if current != None:
            global ticketID
            global dateString
            global counter
            dateString = str(time.strftime("%Y%m%d"))
            ticketID = dateString + "000"
            ticketID = int(ticketID) + counter
            if int(ticketID) <= int(current[0]):
                print("Adjusting the counter...")
                counter+=1
                connectTools.check_count()
            else:
                print("Counter is now in sync!")
        else:
            print("Counter looks good already!")


    def query(table, column):
        """This method allows the user to query which table to access and which
           column in the table. It may be useful, but query_single is more
           useful. It has the ability to display the whole contents of the table
           at half the expense of query_single."""

        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s""", {"table": AsIs(table), "column": AsIs(column)})
        return cursor.fetchall()


    def query_single(table, column, args):
        """This is helpful for when we want to look up an item more specifically.
           We can look up the price from a barcode and other related columns
           prior to making a sale."""
        
        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s WHERE %(args)s;""", {"table": AsIs(table), "column": AsIs(column), "args": AsIs(args)})
        return cursor.fetchone()


    def query_multi(table, column, args):
        """This method was created to return multiple rows from the database. It
           is ideally used to generate reports between different sets of days. It
           is more useful than a plain query."""
        
        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s WHERE %(args)s;""", {"table": AsIs(table), "column": AsIs(column), "args": AsIs(args)})
        return cursor.fetchall()


    def modify_single(table, operation, location):
        """modify_single will do the work of subtracting a number of items from a
           purchase, plus any updates we might have on updating a specific item,
           such as updating a price or setting the sale of an item."""
        
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
        """add_sale has the responsibility to add a row in the sales table, and
           list items associated with that sale."""
        
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
        """add_item will add a new item to the inventory database. It will add
           whatever new item My Tool chooses to carry in the store. It takes the
           arguement of the values of that new row, which are the item_id, the
           quantity, category of the item, price, cost, how many to keep in stock
           regularly, whether the item is on sale or not, the sale start and end
           dates, the sale price, and who supplies that item."""

        global conn
        global cursor
        try:
            cursor.execute(
            """INSERT INTO inventory (item_id, quantity, category, price, cost, desired_quantity, sale, sale_start, sale_end, sale_price, supplier, item_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", row)
            conn.commit()
            return True
        except:
            print("Sorry, I could not add this item")
            return False


    def newMakeSale(itemID):
        """Occurs when user makes a new sale and also checks if the UPC code
           entered is a valid UPC code"""
        
        global itemList
        item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
        if item != None:
            if item[6] == True:
                itemList.append(tuple([itemID, item[11], item[9]]))
            else:
                itemList.append(tuple([itemID, item[11], item[3]]))
        else:
            window = tk.Toplevel()
            window.resizable(width=FALSE,height=FALSE)
            label = Label(window,text="The UPC code you entered was not found in the database!",font="Helvetica 13 bold")
            label.pack(side="top",fill="both",padx=10,pady=10)
            window.after(4000, lambda: window.destroy())
            window.geometry('{}x{}'.format(480,60))


    def voidItem(itemID):
        """This method checks for validity when the user wants to remove an item from their sale.
           And if they input a valid UPC code, it will remove the item"""

        global itemList
        item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
        if item != None:
            if item[6] == True:
                listItem = tuple([itemID, item[11], item[9]])
            else:
                listItem = tuple([itemID, item[11], item[3]])
            if listItem in itemList:
                itemList.remove(listItem)
            else:
                window = tk.Toplevel()
                window.resizable(width=FALSE,height=FALSE)
                label = Label(window,text="The UPC code you entered was not found in the cart!",font="Helvetica 13 bold")
                label.pack(side="top",fill="both",padx=10,pady=10)
                window.after(4000, lambda: window.destroy())
                window.geometry('{}x{}'.format(450,60))
        else:
            window = tk.Toplevel()
            window.resizable(width=FALSE,height=FALSE)
            label = Label(window,text="The UPC code you entered was not found in the database!",font="Helvetica 13 bold")
            label.pack(side="top",fill="both",padx=10,pady=10)
            window.after(4000, lambda: window.destroy())
            window.geometry('{}x{}'.format(480,60))
            
            
    def voidSale():
        """This interacts with our GUI when the user wants to remove their sale"""
        itemList = list()


    def endSale():
        """Used when the user clicks Pay Now!"""
        global subtotal
        global salesTax
        for item in itemList:
            itemIDs.append(item[0])
            itemNames.append(item[1])
            itemPrices.append(item[2])
        sale = list([ticketID, itemIDs, itemPrices])
        if connectTools.add_sale(sale)==False:
            window = tk.Toplevel()
            window.resizable(width=FALSE,height=FALSE)
            label = Label(window,text="The system was unable to submit the sale to the sales database. \
    \nPlease contact IT for more information.",font="Helvetica 13 bold")
            label.pack(side="top",fill="both",padx=10,pady=10)
            window.after(3000, lambda: window.destroy())
            window.geometry('{}x{}'.format(480,60))
        for itemID in itemIDs:
            connectTools.decrement(1, itemID)
        for price in itemPrices:
            subtotal += price
        salesTax = subtotal*.07
        connectTools.generateReceipt(itemNames, itemPrices, subtotal, salesTax)
        window = tk.Toplevel()
        window.resizable(width=FALSE,height=FALSE)
        label = Label(window,text="Sale completed!",font="Helvetica 13 bold")
        label.pack(side="top",fill="both",padx=10,pady=10)
        window.after(3000, lambda: window.destroy())
        window.geometry('{}x{}'.format(480,60))


    def generateReceipt(itemNames, itemPrices, subTotal, salesTax):
        """This new method relies on being called from makeSale(). It takes two
           lists, and two integer values to generate a receipt for the customer.
           It prints out to an excel file with formatted numbers. This is the
           best we have to make a receipt for the cashier. It launches the file
           after it has been created so the customer can print the receipt."""
        
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
        receipt.save('Customer_receipt_' + str(ticketID)+'.xls')
        os.system("start Customer_receipt_" + str(ticketID)+ '.xls')


    def generateWorth():
        """This single method generates the worth of the current inventory. It
           lists out what is currently in the inventory, how many are in stock,
           and what the total worth is for each type of item."""

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
        """Generate worth is still incomplete. It can generate daily reports from
           the current day and yesterday, but only if sales were made on both of
           the days. For testing, I had to check sales from 3 days before,
           because we hadn't populated it with sales for some days. It is also
           not as specific as we planned. It is a very powerful method, but the
           report could include more details. It grabs data from both the sales
           table, and the inventory table to form a complete report."""
        
        global GENERATE_DAILY_REPORT_NAME
        global DATE_CELL
        yesterdays_date = ((datetime.now() - timedelta(days=1)).strftime("%Y%m%d") + "000")
        todays_date = str(time.strftime("%Y%m%d")) + "000"
        sales_today = 0
        sales_yesterday = 0
        profit_today = 0
        profit_yesterday = 0
        today = connectTools.parse_list(connectTools.query_multi('sales', '*', "sale_id >= " + todays_date))
        yesterday = connectTools.parse_list(connectTools.query_multi('sales', '*', "sale_id BETWEEN " + yesterdays_date + " AND " + todays_date))
        COLUMN_HEADINGS = [("Sales Today"), ("Sales Yesterday"),
                           ("Profit Today"), ("Profit Yesterday")]
        report = xlwt.Workbook()
        dailyOperations = report.add_sheet("Worksheet")
        dailyOperations.write_merge(0, 1, 0, 3, GENERATE_DAILY_REPORT_NAME,
                                    BRAND_CELL)
        for x in range(0, len(COLUMN_HEADINGS)):
            dailyOperations.write(2,x, COLUMN_HEADINGS[x], BOLDED_CENTER)
            column = dailyOperations.col(x)
            column.width = 256*25
        for x in range (0, len(today[2])):
            sales_today += (int(today[2][x]))
            profit_today += connectTools.query_single("inventory", "cost", "item_id = " + str(today[1][x]))[0]
        for x in range(0, len(yesterday[2])):
            sales_yesterday +=(int(yesterday[2][x]))
            profit_yesterday += connectTools.query_single("inventory", "cost", "item_id = " + str(yesterday[1][x]))[0]
        dailyOperations.write(3,0, (sales_today/100), MONEY_FORMAT)
        dailyOperations.write(3,1, (sales_yesterday/100), MONEY_FORMAT)
        dailyOperations.write(3,2, (sales_today-profit_today)/100, MONEY_FORMAT)
        dailyOperations.write(3,3, (sales_yesterday-profit_yesterday)/100, MONEY_FORMAT)
        report.save(GENERATE_DAILY_REPORT_NAME+ '.xls')
        os.system("start " + GENERATE_DAILY_REPORT_NAME + '.xls')

        

    def parse_list(alist):
        """This parse list method is specifically called for making the daily
           reports. It has a very specific function and has many limitations. The
           lists that were sent to the database did not have the same structure
           when we pulled them back from the database. So we had to clean them up
           before we could use the data provided. It takes a list of lists as an
           argument and seperates the initial list into sale IDs, then it
           combines all the items sold in that day, and lastly it combines all
           the sale prices. So the end result is the same thing, but it is easier
           to read in Python."""
        
        newList = list()
        item_ids = list()
        item_prices = list()
        sale_ids = list()
        newList.append(sale_ids)
        newList.append(item_ids)
        newList.append(item_prices)
        individual_item = ""
        for row in range(0,len(alist)):
            newList[0].append(alist[row][0])
            for index in range(1,3):
                individual_item = ""
                for character in alist[row][index]:
                    if character == ',':
                        newList[index].append(individual_item)
                        individual_item = ""
                    elif character == '{':
                        pass
                    elif character == '}':
                        newList[index].append(individual_item)
                        pass
                    elif character == ' ':
                        pass
                    else:
                        individual_item += character
        return newList    

    
    def decrement(subtract, itemID):
        """decrement() changes the quantity of an item in a database. There is
           not much important about this yet."""
        
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
        """increment() changes the quanity of an item in a database. We can use this
           to do returns on items."""
        
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

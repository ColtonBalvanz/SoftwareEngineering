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
            print("I am unable to connect to the database")

    def disconnect():
        global conn
        conn.close()

    def query(table, column):

        global cursor
        cursor.execute("""SELECT %(column)s FROM %(table)s""", {"table": AsIs(table), "column": AsIs(column)})
        records = cursor.fetchall()
        pprint.pprint(records)

            
    def modify(table, data, stuff):
        try:
            global cursor
            cursor.execute("UPDATE " + table + "\n\tSET " + data + "\n\tWHERE " + stuff)
        except:
            print("Sorry, I could not modify")
            
##      def makesale():

    def add_item(row):

        global conn
        global cursor
        cursor.execute(
        """INSERT INTO inventory (item_id, quantity, category, price, cost, desired_quantity, sale, sale_start, sale_end, sale_price, supplier)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", row)
        conn.commit()


def main():
    column_name = "item_id"
    table_name = "inventory"
    list1 = (12000151200, 10, 'beverage', 189, 150, 5, None, None, None, None, 'MY TOOL INC')
    connectTools.connect()
    connectTools.query(table_name, column_name)
##    connectTools.add_item(list1)
    connectTools.disconnect()

if __name__ == '__main__':
    main()

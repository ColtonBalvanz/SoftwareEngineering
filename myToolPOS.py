import sys
import pprint
import psycopg2
import urllib.parse
import time


## class GUI
##      global upccode



class connectTools:
    conn = None
    server_info = None
    url = None

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
            cursor = conn.cursor()
            cursor.execute("SELECT * from inventory")
            records = cursor.fetchall()
            pprint.pprint(records)
            conn.close()
        except:
            print("I am unable to connect to the database")

##      def modify(stuff):
##      def query(stuff):
##      def makesale():
##      def add_item(stuff):
##      def remove_item(stuff):


def main():
    connectTools.connect()

if __name__ == '__main__':
    main()

import time

dateString = str(time.strftime("%Y%m%d"))
counter = 0

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
            #check item exixts
            #retrieve item name and price
            #add to receiptString
    #submit to sales db
    #decrement inventory
    print(ticketID)
    print("Thanks for shopping at My Tool!")
    print("Have a great day!")
    print(receiptString)
    

    

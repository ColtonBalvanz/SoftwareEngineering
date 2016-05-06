    def makeSale():
        """The makeSale() method is responsible for producing the sale of a
           customer. It will also print out a physical receipt the customer can
           take with them."""
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

def newMakeSale(itemID):
    item = connectTools.query_single("inventory", "*", "item_id = " + itemID)
    if item != None:
        return tuple(itemID, item[11], item[9])
    else:
       return tuple(None, None, None)

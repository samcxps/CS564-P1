
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def fixQuotation(str_input):
    str_input = str_input.replace('"','""')
    str_input = '"' + str_input + '"'
    return str_input

def get_item(item):
    item_id = item["ItemID"]                    # primary key
    name = fixQuotation(item["Name"])
    currently = transformDollar(item["Currently"])
    buy_price = transformDollar(item["Buy_Price"]) if item.get("Buy_Price") else "NULL"
    first_bid = transformDollar(item["First_Bid"])
    number_of_bids = item["Number_of_Bids"]
    started = transformDttm(item["Started"])
    ends = transformDttm(item["Ends"])
    seller = item["Seller"]["UserID"]                     # foreign key
    description = fixQuotation(item["Description"]) if item.get("Description") else "NULL"

    tmp_str = item_id + "|" + name + "|" + currently + "|" + buy_price + "|" + first_bid + "|" + number_of_bids + "|" + started + "|" + ends + "|" + seller + "|" + description

    return tmp_str
Sellers = set()
Bidders = set()
def get_user(item):
    ret_users = set()
    ret_sellers = set()
    ret_bidders = set()
    #### Seller user stuff
    user_id = item["Seller"]["UserID"]
    rating = item["Seller"]["Rating"]
    country = item["Country"] if item["Country"] else "NULL"
    location = fixQuotation(item["Location"]) if item["Location"] else "NULL"
    if user_id not in Sellers and user_id not in Bidders:
        ret_users.add(user_id + "|" + rating + "|" + country + "|" + location)
    if user_id not in Sellers:
        ret_sellers.add(user_id)
        Sellers.add(user_id)
    ####
    #### Bid user stuff
    item_bids = item.get('Bids')
    if item_bids:
        for bid in item_bids:
            user_id = bid["Bid"]["Bidder"]["UserID"]
            rating = bid["Bid"]["Bidder"]["Rating"]
            country = bid["Bid"]["Bidder"]["Country"] if bid.get("Bid").get("Bidder").get("Country") else "NULL"
            location = fixQuotation(bid["Bid"]["Bidder"]["Location"]) if bid.get("Bid").get("Bidder").get("Location") else "NULL"
            if user_id not in Sellers and user_id not in Bidders:
                ret_users.add(user_id + "|" + rating + "|" + country + "|" + location)
            if user_id not in Bidders:  
                ret_bidders.add(user_id)
                Bidders.add(user_id)

    return ret_users, ret_sellers, ret_bidders


def get_bid(item):
    tmp_bids = []
    item_bids = item.get('Bids')

    if item_bids:
        for bid in item_bids:
            item_id = item["ItemID"] 
            user_id = bid["Bid"]["Bidder"]["UserID"]
            time = transformDttm(bid["Bid"]["Time"])
            amount = transformDollar(bid["Bid"]["Amount"])

            tmp_str = item_id + "|" + user_id + "|" + time + "|" + amount

            tmp_bids.append(tmp_str.encode('utf-8'))

    return tmp_bids

def get_category(item):
    tmp_cat = []
    item_categories = set(item["Category"])
    item_id = item["ItemID"] 

    tmp_str = item_id + "|"
    for category in item_categories:
        tmp_str = tmp_str + category + '|'
    max_cat_size = 6
    cat_size = len(item_categories)
    null_cat = max_cat_size - cat_size
    for i in range(null_cat):
        tmp_str = tmp_str + 'NULL' + '|'
    tmp_str = tmp_str + str(len(item_categories))

    tmp_cat.append(tmp_str.encode('utf-8'))

    return tmp_cat


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    item_dat = []
    seller_dat = []
    bidder_dat = []
    user_dat = []
    bid_dat = []
    category_dat = []

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        i = 0
        for item in items:
            item_dat.append(get_item(item))
            bid_dat.append(get_bid(item))
            category_dat.append(get_category(item))

            items_user, sellers, bidders = get_user(item)
            for user in items_user:
                user_dat.append(user)
            items_sellers = sellers
            for user in items_sellers:
                seller_dat.append(user)
            items_bidders = bidders
            for user in items_bidders:
                bidder_dat.append(user)

    strng = '\n'
    str_byte = str.encode(strng)

    with open("dat_files/user.dat", 'ab') as f:
        for user in user_dat:
            f.write(user.encode())
            f.write(str_byte)
    
    with open("dat_files/seller.dat", 'ab') as f:
        for user in seller_dat:
            f.write(user.encode())
            f.write(str_byte)

    with open("dat_files/bidder.dat", 'ab') as f:
        for user in bidder_dat:
            f.write(user.encode())
            f.write(str_byte)

    with open("dat_files/item.dat", 'ab') as f:
        for item in item_dat:
            f.write(item.encode())
            f.write(str_byte)

    with open("dat_files/bid.dat", 'ab') as f:
        for bid in bid_dat:
            for b in bid:
                f.write(b)
                f.write(str_byte)

    with open("dat_files/category.dat", 'ab') as f:
        for cat in category_dat:
            for c in cat:
                f.write(c)
                f.write(str_byte)
                


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)

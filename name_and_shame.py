#!/usr/bin/env python3
import os
import json

from ebaysdk.finding import Connection


"""
things_people_need
    "face shield",
    "n95 mask",
    "n100 mask",
    "toilet paper",
    "hand sanitizer",
    "disinfectant"
    "rubbing alcohol",
    "isopropyl alcohol",
    "baby wipes",
    "first aid kit",
    "hydrogen peroxide",
    "antiseptic",
    "paper towels",

"""

APPID = os.environ["EBAY_APPID"]
EBAY_CATEGORY_MAP = {
    "toilet paper": 179204,
}

def pretty_please(d):
    print(json.dumps(d, indent=2, separators=(",", ":")))

api = Connection(appid=APPID, config_file=None, debug=True)

def find(category_id):
    req_params = {
        "keywords": "toilet paper",
        "sortOrder": "PricePlusShippingHighest",
        "outputSelector": "SellerInfo",
        "categoryId": 179204,
    }

    res = api.execute("findItemsAdvanced", req_params)

    return res.dict()["searchResult"]["item"]

def listing_is_bullshit(listing):
    if float(listing["sellingStatus"]["currentPrice"]["value"]) > 100:
        return True
    return False

def name_and_shame(listing):
    return {
        "title": listing["title"],
        "seller": listing["sellerInfo"],
        "price": listing["sellingStatus"]["currentPrice"]["value"],
        "url": listing["viewItemURL"],
    }

def process_listings(listings):
    return sorted(
        [name_and_shame(listing) for listing in listings if listing_is_bullshit(listing)],
        key=lambda e: e["price"]
    )

if __name__ == "__main__":
    listings = find(EBAY_CATEGORY_MAP["toilet paper"])
    gougers = process_listings(listings)

pretty_please(gougers)

# venv\scripts\activate          on cmd to start venv
# python server.py (name of file) to start server
from ftplib import all_errors
from math import prod
from flask import Flask, abort, request
import json
from mock_data import catalog
from config import db
from bson import ObjectId

app = Flask("Server")


@app.route("/")
def home():
    return "Hello from Flask"



@app.route("/me")
def about_me():
    return "Sebastian Ruiz"


##########################################
############  API ENDPOINTs   ############ 
############  RETURN Json  ###############
##########################################


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    
    products = []
    cursor = db.products.find({}) # Cursor is a collection

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        products.append(prod)

    return json.dumps(products)



@app.route("/api/catalog", methods=["POST"])
def save_catalog():
    product = request.get_json() # Return the data (payload) from the request
    
    db.products.insert_one(product)
    print(product)

    # Fix _id
    product["_id"] = str(product["_id"])

    return json.dumps(product)



# /api/catalog/count -> how manu products exist in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def noProd_catalog():
    cursor = db.products.find({}) # Cursor is a collection
    count = 0
    for prod in cursor:
        count += 1
    return json.dumps(count)

@app.route("/api/catalog/total", methods=["GET"])
def total_of_catalog():
    sumT = 0
    cursor = db.products.find({})
    for product in cursor:
        sumT = sumT + product["price"]
    
    return json.dumps(f"Sum of prices {sumT}")

@app.route("/api/product/<id>")
def got_by_id(id):
    
    prod = db.products.find_one({"_id": ObjectId(id)})

    if not prod:
        return abort(404, "No product with that ID was found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)
    
    # NOT FOUND: Error 404
    

@app.route("/api/product/cheapest", methods=["GET"])
def lowest_product():

    lowest = catalog[0]
    for product in catalog:
        if product["price"] < lowest["price"]:
            lowest = product
    return json.dumps(f"Cheapest product {lowest}")


@app.route("/api/categories", methods=["GET"])
def unique_categories():
    categories = []
    for prod in catalog:
        category = prod["category"]

        if not category in categories:
            categories.append(category)

    return json.dumps(f"Categories: {categories}")


# 
# Ticket 2345
# Creat and endpoint that allow the client to get all the products
# for an specified category
# /api/catalog/guitar where guitar is the category in question
# 

@app.route("/api/catalog/<category>")
def product_category(category):

    products = []
    cursor = db.products.find({"category": category})

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        products.append(prod)

    return json.dumps(products)

@app.route("/api/someNumbers", methods=["GET"])
def some_numbers():
    num=[]
    for i in range (1, 51):
        num.append(i)
    return json.dumps(f"Number: {num}")


###########################################
########## Coupon Code EndPoints ##########
###########################################
# 1 Get all coupons
# 2 Save coupon
# 3 Get a coupon based on its code


@app.route("/api/couponCode", methods=["GET"])
def get_coupon():

    coupons = []
    cursor = db.coupons.find({})

    for coup in cursor:
        coup["_id"] = str(coup["_id"])
        coupons.append(coup)
    return json.dumps(coupons)


@app.route("/api/couponCode", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    
    db.coupons.insert_one(coupon)
    print(coupon)

    # Fix _id
    coupon["_id"] = str(coupon["_id"])

    return json.dumps(coupon)

@app.route("/api/couponCode/<code>")
def coupon_code(code):

    coup = db.coupons.find_one({"code": code})
    
    if not coup:
        return abort(404, "No product with that CODE Found")
    coup["_id"] = str(coup["_id"])
    return json.dumps(coup)



app.run(debug=True)


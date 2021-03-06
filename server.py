# venv\scripts\activate          on cmd to start venv
# python server.py (name of file) to start server
from ftplib import all_errors
from math import prod
from flask import Flask, abort, request
import json
from mock_data import catalog
from config import db
from bson import ObjectId
from flask_cors import CORS

app = Flask("Server")
CORS(app)

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

    if not "code" in coupon or len(coupon["code"]) < 5 :
        return abort(400, "code is required to have at least 5 characters for coupon registration")
   

    if not "discount" in coupon or coupon["discount"] > 50 or coupon["discount"]< 5:
        return abort(400, "Coupon is required and it needs to be higher than 5% and lower than 50%")

    


    
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



###########################################
########## Users EndPoints ################
###########################################

@app.route("/api/users", methods=["GET"])
def get_user():

    users = []
    cursor = db.users.find({})

    for usr in cursor:
        usr["_id"] = str(usr["_id"])
        users.append(usr)
    return json.dumps(users)

@app.route("/api/users", methods=["POST"])
def save_user():
    user = request.get_json()


    if not "userName" in user or len(user["userName"]) < 1:
        return abort(400, "UserName is required for user registration")

    if not "password" in user or len(user["password"]) < 1:
        return abort(400, "password is required for user registration")
    
    if not "email" in user or len(user["email"]) < 1:
        return abort(400, "email is required for user registration")
    
    db.users.insert_one(user)
    print(user)

    # Fix _id
    user["_id"] = str(user["_id"])

    return json.dumps(user)

@app.route("/api/users/<email>")
def user_email(email):

    usr = db.users.find_one({"email": email})
    
    if not usr:
        return abort(404, "No user with that email Found")
    usr["_id"] = str(usr["_id"])
    return json.dumps(usr)

@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json()
    print(data)

    if not "user" in data:
        return abort(400, "User is required for login")
    
    if not "password" in data:
        return abort(400, "Password is required for login")

    usr = db.users.find_one({"userName": data["user"], "password": data["password"]})
    if not usr:
        abort(401, "User or Password Incorrect")
    
    usr["_id"] = str(usr["_id"])
    usr

    usr.pop("password")

    return json.dumps(usr)

    

# login is done in a post, userName and Password


app.run(debug=True)


from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource
import pymongo
import json
from bson.objectid import ObjectId

# create app
app = Flask(__name__)

# connect to db
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
        )
    db = mongo.crawl
    mongo.server_info()  # trigger exception if db connection failed
except:
    print("ERROR - cannot connect to db")

# Brands - zalando & omoda
@app.route("/competitor_zalando", methods = ["GET"])
def get_zalando():
    """ This function fetches competitor's brand """

    competitor_details = {
        "_id": 0,
        "competitor": "zalando",
        "zalando_info.brand_name": 1
    }
    try:
        data = list(db.productdetail.find({}, competitor_details))
        for comp in data:
            comp["competitor"] = str(comp["competitor"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print("------------------ERROR--------------------")
        print(ex)
        print("-------------------END---------------------")
        return Response(
            response=json.dumps({"message": "competitor zalando cannot be fetched."}),
            status=500,
            mimetype= "application/json"
        )

@app.route("/competitor_omoda", methods=["GET"])
def get_omoda():
    """ This function fetches competitor's brand """
    competitor_details = {
        "_id": 0,
        "competitor": "omoda",
        "omoda_info.brand_name": 1
    }
    try:
        data = list(db.productdetail.find({}, competitor_details))
        for comp in data:
            comp["competitor"] = str(comp["competitor"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print("------------------ERROR--------------------")
        print(ex)
        print("-------------------END---------------------")
        return Response(
            response=json.dumps({"message": "competitor omoda cannot be fetched."}),
            status=500,
            mimetype= "application/json"
        )

# Sites
@app.route("/sites", methods=["GET"])
def get_sites():
    """ This function retrieves URLS """
    sites = {
        "_id": 0,
        "page_url": 1
    }

    try:
        data = list(db.productdetail.find({}, sites))
        for site in data:
            site["page_url"] = str(site["page_url"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print("------------------ERROR--------------------")
        print(ex)
        print("-------------------END---------------------")
        return Response(
            response=json.dumps({"message": "sites cannot be fetched."}),
            status=500,
            mimetype= "application/json"
        )

# Products of a given brand.
@app.route("/brands/<brand>", methods = ["GET"])
def get_brands(brand):
    """ This function retrieves URLS """
    brand = str(brand)
    brands = {
        "_id": 0,
        "zalando_info.brand_name": brand,
        "zalando_info.product_name": 1,
        "competitor": 1
    }

    try:
        data = list(db.productdetail.find({}, brands))
        for brand_res in data:
            if "zalando" in brand_res["competitor"]:
                brand_res["zalando_info"]["product_name"] = str(brand_res["zalando_info"]["product_name"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print("------------------ERROR--------------------")
        print(ex)
        print("-------------------END---------------------")
        return Response(
            response=json.dumps({"message": "brand cannot be fetched."}),
            status=500,
            mimetype= "application/json"
        )


# Fetch product details
@app.route("/brand_productdetails/<prod>", methods = ["GET"])
def get_productdetails(prod):
    """ This function retrieves product details """
    prod = str(prod)
    productdetails = {
        "_id": 0,
        "zalando_info.product_name": '/' + prod + '/',
        "zalando_info.product_type": 1,
        "zalando_info.brand_name": 1,
        "zalando_info.price": 1,
        "product_url": 1,
        "competitor": 1
    }

    try:
        data = list(db.productdetail.find({}, productdetails))
        for proddet in data:
            if "zalando" in proddet["competitor"]:
                proddet["zalando_info"]["product_name"] = str(proddet["zalando_info"]["product_name"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print("------------------ERROR--------------------")
        print(ex)
        print("-------------------END---------------------")
        return Response(
            response=json.dumps({"message": "brand cannot be fetched."}),
            status=500,
            mimetype= "application/json"
        )

"""
@app.route("/brand_productdetailsomoda/<prod>", methods = ["GET"])
def get_productdetailsomoda(prod):

    prod = str(prod)
    productdetails = {
        "_id": 0,
        "omoda_info.pname_cat": '/' + '^' + prod + '/',
        "omoda_info.pname": 1,
        "omoda_info.brand_name": 1,
        "omoda_info.cost_ext": 1,
        "omoda_info.cost_dis": 1,
        "product_url": 1,
        "competitor": "omoda"
    }

    try:
        data = list(db.productdetail.find({}, productdetails))
        for proddet in data:
            if "omoda" in proddet["competitor"]:
                proddet["omoda_info"]["pname_cat"] = str(proddet["omoda_info"]["pname_cat"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print("------------------ERROR--------------------")
        print(ex)
        print("-------------------END---------------------")
        return Response(
            response=json.dumps({"message": "brand cannot be fetched."}),
            status=500,
            mimetype= "application/json"
        )
"""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
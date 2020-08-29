from application import api
from application.resources.product import Product, Products
from application.resources.offer import Offer, Offers

api.add_resource(Product, "/product/<string:name>")  # GET, POST, DELETE, PUT - calls to local database
api.add_resource(Products, "/products")  # GET all products from local database.
api.add_resource(Offer, "/offer/<int:id>")  # POST call to the Offers API microservice.
api.add_resource(Offers, "/offers")  # GET all offers from local database

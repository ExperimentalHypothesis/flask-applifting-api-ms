import requests
from db import db
# from flask import current_app as app
from application import create_app
from sqlalchemy.exc import OperationalError

app = create_app()


class OfferModel(db.Model):
    """ Data model for offers. """

    __tablename__ = "Offers"
    pk_id = db.Column(db.Integer, primary_key=True, unique=True)
    offer_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    items_in_stock = db.Column(db.Integer)
    product = db.relationship("ProductModel")
    product_id = db.Column(db.Integer, db.ForeignKey("Products.product_id"))  # backref one-to-many link

    offer_ids = []

    def __init__(self, id, price, items_in_stock, product_id):
        self.offer_id = id
        self.price = price
        self.items_in_stock = items_in_stock
        self.product_id = product_id

    def __repr__(self):
        return f"<OfferModel {self.offer_id}>"

    @classmethod
    def call_offer_api(cls, id: int) -> list:
        """ Give me the offers for products I registered in external offers API microservice. """
        with app.app_context():
            offers_url = app.config["MS_API_OFFERS_BASE_URL"] + "/products/" + str(id) + "/offers"
            headers = {"Bearer": app.config["MS_API_ACCESS_TOKEN"]}
            res = requests.get(offers_url, headers=headers).json()
            return res

    @classmethod
    def update_offer_price(cls):
        """ Keep calling external offers API microservice to get new prices. This function will run in a separated thread in a scheduler. """
        with app.app_context():
            headers = {"Bearer": app.config["MS_API_ACCESS_TOKEN"]}
            for offer_id in OfferModel.offer_ids:
                print(offer_id)
                offers_url = app.config["MS_API_OFFERS_BASE_URL"] + "/products/" + str(offer_id) + "/offers"
                res = requests.get(offers_url, headers=headers).json()
                print(f"getting updated price for id: {offer_id}\n {res}")
                for offer in res:
                    try:
                        OfferModel.query.filter_by(offer_id=offer["id"]).update(dict(price=offer["price"]))
                        db.session.commit()
                    except OperationalError:
                        print("Database does not exists.")
                        db.session.rollback()

    @classmethod
    def find_by(cls, offer_id: int):
        """ Find product by offer_id. """
        return cls.query.filter_by(offer_id=offer_id).first()

    def make_json(self):
        """ Make JSON from the object. """
        return {"offer_id": self.offer_id,
                "price": self.price,
                "items_in_stock": self.items_in_stock,
                "product_id": self.product_id}

    def save_to_db(self):
        """ Save offer to database. """
        db.session.add(self)
        db.session.commit()


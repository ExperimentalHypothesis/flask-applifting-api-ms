import requests
from db import db
from flask import current_app as app
from application.models.offer import OfferModel


class ProductModel(db.Model):
    """ Data model representing a product. """

    __tablename__ = "Products"
    pk_id = db.Column(db.Integer, primary_key=True, unique=True)
    product_id = db.Column(db.Integer)  # id for one-to-many link
    name = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    offers = db.relationship("OfferModel", uselist=False)

    def __init__(self, name, description):
        self.product_id = app.config["MS_API_ID"]
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<ProductModel {self.name}>"

    @classmethod
    def find_by(cls, name: str):
        """ Find product by name. """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def register_product(cls, data: dict):
        """ Register product in offer MS API. """
        register_url = app.config["MS_API_OFFERS_BASE_URL"] + "/products/register"
        data = {**data, "id": app.config["MS_API_ID"]}
        headers = {"Bearer": app.config["MS_API_ACCESS_TOKEN"]}
        res = requests.post(register_url, data=data, headers=headers)
        print(f"product registered with id {res.json().get('id')}")
        OfferModel.offer_ids.append(app.config["MS_API_ID"])
        print("list of registered ids: ", OfferModel.offer_ids)
        app.config["MS_API_ID"] += 1


    def make_json(self):
        """ Make JSON from the object. """
        return {"product_id": self.product_id,
                "name": self.name,
                "description": self.description}

    def save_to_db(self):
        """ Save product to database. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ Delete product from database. """
        db.session.delete(self)
        db.session.commit()
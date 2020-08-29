from flask_restful import Resource, reqparse
from flask import current_app as app
from application.models.product import ProductModel


class Product(Resource):
    """ Resource for one product. """

    parser = reqparse.RequestParser()
    parser.add_argument("description", type=str, required=True, help="product description.")

    def get(self, name: str):
        """ Endpoint for getting product from local database."""
        try:
            product = ProductModel.find_by(name)
        except:
            return {"msg": "server error"}, 500

        if product:
            return product.make_json(), 200
        return {"msg": f"product '{name}' not found"}, 404

    # TODO unauthorized
    def post(self, name: str):
        """ Endpoint for creating a product and saving it to local database. """
        data = Product.parser.parse_args()
        new_product = ProductModel(name, data["description"])

        try:
            if ProductModel.find_by(name):
                return {"msg": f"product '{name}' already exists"}, 400  # BAD REQUEST
        except:
            return {"msg": "server error"}, 500
        else:
            try:
                new_product.save_to_db()
                ProductModel.register_product(data)
                return {"msg": f"product '{name}' created & registered with id: {app.config['MS_API_ID'] - 1}"}, 201  # OK
            except Exception as e:
                return {"msg": f"server error {e}"}, 500

    # TODO authorized
    def delete(self, name: str):
        """ Endpoint for deleting a product from local database. """
        try:
            product = ProductModel.find_by(name)
        except:
            return {"msg": "server error"}, 500

        if product:
            product.delete_from_db()
            return {"msg": f"product '{name}' deleted"}, 200  # OK
        return {"msg": f"product '{name}' not found"}, 404

    # TODO authorizes
    def put(self, name: str):
        """ Endpoint for updating a product in local database. """
        data = Product.parser.parse_args()

        try:
            product = ProductModel.find_by(name)
        except:
            return {"msg": "server error"}, 500

        if product:
            product.description = data["description"]
            product.save_to_db()
            return {"msg": f"product '{name}' updated"}, 200
        else:
            product = ProductModel(name, data["description"])
            product.save_to_db()
            ProductModel.register_product(data)
            return {"msg": f"product '{name}' created & registered with id: {app.config['MS_API_ID'] - 1}"}, 201  # OK


class Products(Resource):
    """ Resource for all products. """

    def get(self):
        """ Endpoint for getting all products from local database. """
        return {"products": [i.make_json() for i in ProductModel.query.all()]}, 200  # OK


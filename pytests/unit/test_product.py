from flask import current_app as app
from application.models.product import ProductModel


def test_create_product(test_client_no_db):
    """
    GIVEN a Flask application
    WHEN a Product is instantiated
    THEN check the properties are valid
    """
    p = ProductModel("testing name", "testing description")
    assert p.product_id == app.config["MS_API_ID"]
    assert p.name == "testing name"
    assert p.description == "testing description"


def test_make_json(test_client_no_db):
    """
    GIVEN a Flask application and Product is instantiated
    WHEN called make_json()
    THEN check the output is correct
    """
    p = ProductModel("testing name", "testing description")
    expecting = {"product_id": app.config["MS_API_ID"],
                 "name": "testing name",
                 "description": "testing description"}
    assert p.make_json() == expecting

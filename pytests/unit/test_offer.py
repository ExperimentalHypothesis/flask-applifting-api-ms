from application.models.offer import OfferModel

def test_create_offer(test_client_no_db):
    """
     GIVEN a Flask application
     WHEN an offer is instantiated
     THEN check the properties are valid
     """
    o = OfferModel(1, 1000, 93, 4)
    assert o.offer_id == 1
    assert o.price == 1000
    assert o.items_in_stock == 93
    assert o.product_id == 4


def test_make_json(test_client_no_db):
    """
    GIVEN a Flask application and Offer is instantiated
    WHEN called make_json()
    THEN check the output is correct
    """
    o = OfferModel(1, 1000, 93, 4)
    expecting = {"offer_id": 1,
                 "price": 1000,
                 "items_in_stock": 93,
                 "product_id": 4}
    assert o.make_json() == expecting
from application.models.product import ProductModel

def test_save_and_delete(test_client_db):
    """
    GIVEN a Flask application and a new database
    WHEN new product is instantiated,
    FIRST check it is not in the database
    THEN save it to database and check it is there
    THEN delete it and check it is not there
    """
    p = ProductModel("some name", "some description")
    assert ProductModel.find_by(p.name) is None
    p.save_to_db()
    assert ProductModel.find_by(p.name) is not None
    p.delete_from_db()
    assert ProductModel.find_by(p.name) is None
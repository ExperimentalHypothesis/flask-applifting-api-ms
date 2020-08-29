from application.models.product import ProductModel


def test_save_and_delete(test_client_db):
    p = ProductModel("some name", "some description")
    assert ProductModel.find_by(p.name) is None
    p.save_to_db()
    assert ProductModel.find_by(p.name) is not None
    p.delete_from_db()
    assert ProductModel.find_by(p.name) is None
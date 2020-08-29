import json
from application.models.product import ProductModel
from flask import current_app as app


def test_get_all_products(test_client_db):
    res = test_client_db.get('/products')
    assert res.status_code == 200


def test_get_product_not_found(test_client_db):
    res = test_client_db.get("/product/test")
    assert res.status_code == 404
    assert json.loads(res.data) == {"msg": "product 'test' not found"}


def test_get_product_found(test_client_db):
    p = ProductModel("test", "testing")
    p.save_to_db()
    res = test_client_db.get("product/test")
    assert res.status_code == 200
    assert json.loads(res.data) == p.make_json()


def test_create_product(test_client_db):
    res = test_client_db.post("product/testing", data={"description": "testing"})  # TODO tady kdzy dam /test tak mi to spadne protoze uz v DB je.. chtelo by to na kazdej test jit s cistou DB
    assert res.status_code == 201
    assert json.loads(res.data) == {"msg": f"product 'testing' created & registered with id: {app.config['MS_API_ID'] - 1}"}


def test_create_duplicate_product(test_client_db):
    first = test_client_db.post("product/new_product", data={"description": "description of the new product"})
    assert first.status_code == 201
    second = test_client_db.post("product/new_product", data={"description": "description of the new product"})
    assert second.status_code == 400
    assert json.loads(second.data) == {"msg": f"product 'new_product' already exists"}


def test_delete_existing_product(test_client_db):
    res_insert = test_client_db.post("product/another_product", data={"description": "description of product"})
    assert res_insert.status_code == 201
    res_del = test_client_db.delete("product/another_product")
    assert res_del.status_code == 200
    assert json.loads(res_del.data) == {"msg": f"product 'another_product' deleted"}


def test_delete_nonexisting_product(test_client_db):
    res = test_client_db.delete("product/produkt_kterej_tam_neni")
    assert res.status_code == 404
    assert json.loads(res.data) == {"msg": f"product 'produkt_kterej_tam_neni' not found"}


def test_update_existing_product(test_client_db):
    res_post = test_client_db.post("product/walkman", data={"description": "nejlepsi walkman"})
    assert res_post.status_code == 201
    res_put = test_client_db.put("product/walkman", data={"description": "nejlepsi walkman pro audiofily"})
    assert res_put.status_code == 200
    assert json.loads(res_put.data) == {"msg": f"product 'walkman' updated"}


def test_update_nonexisting_product(test_client_db):
    res = test_client_db.put("product/discman", data={"description": "nejlepsi discman pro audiofily"})
    assert res.status_code == 201
    assert json.loads(res.data) == {"msg": f"product 'discman' created & registered with id: {app.config['MS_API_ID'] - 1}"}




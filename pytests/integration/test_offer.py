from application.models.offer import OfferModel


def test_save(test_client_db):
    o = OfferModel(1, 1000, 93, 4)
    assert OfferModel.find_by(o.offer_id) is None
    o.save_to_db()
    assert OfferModel.find_by(o.offer_id) is not None
    found_offer = OfferModel.find_by(o.offer_id)
    assert found_offer.price == 1000
    assert found_offer.items_in_stock == 93

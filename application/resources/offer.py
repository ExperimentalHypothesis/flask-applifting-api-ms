from flask_restful import Resource
from application.models.offer import OfferModel


class Offer(Resource):
    """ Resource for offer. """

    def post(self, id: int):
        """ Endpoint for retrieving offers from offer MS and saving them in local database. """
        try:
            offers = OfferModel.call_offer_api(id)
        except:
            return {"msg": "server error. wrong id in the url? [do GET /offers/ids to see all url ids]"}, 500
        else:
            if offers:
                for offer in offers:
                    o = OfferModel(**offer, product_id=id)
                    o.save_to_db()
                return {"offers": offers}, 200
            else:
                return {"msg": "no offers"}, 404


class Offers(Resource):
    """ Resource for offer. """

    def get(self):
        """ Endpoint for getting all offers from local database. """
        return {"offers": [i.make_json() for i in OfferModel.query.all()]}
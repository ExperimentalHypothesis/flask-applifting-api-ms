import requests, threading
from application import scheduler, create_app
from application.models.offer import OfferModel

app = create_app()

if __name__ == "__main__":
    @app.before_first_request
    def get_token():
        res = requests.post(app.config["MS_API_OFFERS_BASE_URL"] + "/auth").json()
        app.config["MS_API_ACCESS_TOKEN"] = res.get("access_token")

    scheduler.add_job(id="Check updated price", func=OfferModel.update_offer_price, trigger="interval", seconds=60)
    threading.Thread(target=scheduler.start).start()

    app.run(debug=True, use_reloader=False)

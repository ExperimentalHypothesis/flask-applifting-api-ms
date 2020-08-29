from flask import Flask
from flask_restful import Api
from flask_apscheduler import APScheduler
from db import db

api = Api()
scheduler = APScheduler()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)
    api.init_app(app)
    scheduler.init_app(app)
    
    with app.app_context():
        db.create_all()

        return app


from application import endpoints  # importing here to avoid circular imports


import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    # general config
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # database config
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # offers api config
    MS_API_OFFERS_BASE_URL = os.environ.get("MS_API_OFFERS_BASE_URL")
    MS_API_ACCESS_TOKEN = os.environ.get("MS_API_ACCESS_TOKEN")
    MS_API_ID = 1010
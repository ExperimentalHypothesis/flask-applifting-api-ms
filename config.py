

class Config:
    # general config
    SECRET_KEY = "sdjahdjskldfkjsldj"

    # database config
    SQLALCHEMY_DATABASE_URI = "sqlite:///product-data.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # offers api config
    MS_API_OFFERS_BASE_URL = "https://applifting-python-excercise-ms.herokuapp.com/api/v1"
    MS_API_ACCESS_TOKEN = "c4a18b5b-72af-4e3b-b5ed-89959fa475d1"
    MS_API_ID = 1010
import pytest
from application import create_app
from db import db


@pytest.fixture(scope='module')
def test_client_no_db():
    """
    Create the app and prepare app context with testing client.
    """
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def test_client_db():
    """
    Prepare the app with new database.
    Prepare testing client and the context.
    """
    flask_app = create_app()

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()

    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from .products.routes import products_b_p
    app.register_blueprint(products_b_p, url_prefix="/products")

    with app.app_context():
        db.create_all()

    return app

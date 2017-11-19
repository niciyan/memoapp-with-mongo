from flask import Flask
from flask_mongoengine import MongoEngine
from models import db

def create_app():

    app = Flask(__name__)
    db.init_app(app) 

    from views import main
    app.register_blueprint(main)

    app.config["MONGODB_SETTINGS"] = { "db":"nishi" }
    app.config['SECRET_KEY'] = "ok"
    app.debug = True

    return app

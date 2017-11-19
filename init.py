from flask import Flask, render_template, abort, flash
from flask_mongoengine import MongoEngine
from pymongo.errors import PyMongoError
from models import db

def create_app():

    app = Flask(__name__)
    db.init_app(app) 

    from views import main
    app.register_blueprint(main)

    # @app.error_handler(500)
    # def internal_server_error(e):
        
    

    @app.errorhandler(PyMongoError)
    def handle_db_error(error):
        flash("database error occured. Visit later.")
        return render_template('500.html'), 500 

    app.config["MONGODB_SETTINGS"] = { "db":"nishi" }
    app.config['SECRET_KEY'] = "ok"
    app.debug = True

    return app

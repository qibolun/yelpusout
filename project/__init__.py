import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# instantiate the db
db = SQLAlchemy()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.views import users_blueprint
    from project.api.views import group_blueprint
    from project.api.views import votingsession_blueprint
    app.register_blueprint(users_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(votingsession_blueprint)

    return app

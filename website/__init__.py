from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey"
    app.config["UPLOAD_FOLDER"] = "uploads"

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    from .views.views import views
    from .views.dataGen import dataGen

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(dataGen, url_prefix="/")

    return app
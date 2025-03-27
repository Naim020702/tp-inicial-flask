from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey"
    app.config["UPLOAD_FOLDER"] = "uploads"

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    from .views.home import homeView
    from .views.dataGen import dataGenView
    from .views.training import trainingView

    app.register_blueprint(homeView, url_prefix="/")
    app.register_blueprint(dataGenView, url_prefix="/")
    app.register_blueprint(trainingView, url_prefix="/")

    return app
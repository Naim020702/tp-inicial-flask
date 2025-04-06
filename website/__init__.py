# Este archivo es parte de un proyecto de Flask que incluye varias vistas y configuraciones
from flask import Flask
import os

# Funcion para crear la aplicacion de Flask
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey" # Clave secreta para la aplicacion
    app.config["UPLOAD_FOLDER"] = "uploads" # Carpeta para subir archivos

    # Si la carpeta de subida no existe, crearla
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Importacion de las vistas
    from .views.home import homeView
    from .views.dataGen import dataGenView
    from .views.training import trainingView
    from .views.predRes import predResView

    # Registro de las vistas como blueprints, que permiten organizar el codigo en modulos y evistar conflictos de nombres de rutas
    # Cada blueprint tiene su propio conjuntos de rutas y vistas
    app.register_blueprint(homeView, url_prefix="/")
    app.register_blueprint(dataGenView, url_prefix="/")
    app.register_blueprint(trainingView, url_prefix="/")
    app.register_blueprint(predResView, url_prefix="/")

    # Retorna la aplicacion de Flask
    return app
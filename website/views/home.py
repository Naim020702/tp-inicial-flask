# Blueprint para crear la vista de la pagina de inicio
# render_template para renderizas los .html
from flask import Blueprint, render_template

# Crea un blueprint o vista
homeView = Blueprint("home", __name__)

# Ruta para la pagina de inicio. La funcion asociada se ejecuta cuando se accede a la ruta
@homeView.route("/")
def home():
    return render_template("home.html")
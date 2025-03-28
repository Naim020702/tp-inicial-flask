from flask import Blueprint, render_template, flash
from website import shared_data

predResView = Blueprint("predResView", __name__)

@predResView.route("/pred-res")
def pred_res():
    modelo = shared_data.modelo
    X_test = shared_data.X_test
    y_test = shared_data.y_test

    boolean = modelo is not None and X_test is not None and y_test is not None

    if boolean:
        print("X_test: ", X_test)
        flash("Podemos predecir tranquilamente", category="success")
    else:
        flash("No hay datos para predecir", category="error")

    return render_template("pred-res.html")
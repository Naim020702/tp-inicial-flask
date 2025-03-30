from flask import Blueprint, render_template, flash, request
from website.views.generar_matriz_confusion import generar_matriz_confusion
from website.views.generar_curva_sigmoide import generar_curva_sigmoide
from website import shared_data
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

predResView = Blueprint("predResView", __name__)

def realizar_prediccion(modelo, X_test, y_test):
    # Realizar predicciones
    y_pred = modelo.predict(X_test)

    # Calcular métricas
    precision = accuracy_score(y_test, y_pred)
    matriz_confusion = confusion_matrix(y_test, y_pred)
    reporte_clasificacion = classification_report(y_test, y_pred)

    # Generar y guardar la imagen de la matriz de confusión
    ruta_imagen = generar_matriz_confusion(matriz_confusion)

    # Llamar a la función para generar la curva sigmoide
    ruta_curva_sigmoide = generar_curva_sigmoide(modelo, X_test)

    resultados = {
        'precision': precision,
        'matriz_confusion': matriz_confusion,
        'reporte_clasificacion': reporte_clasificacion,
        'ruta_imagen': ruta_imagen, 
        'ruta_curva_sigmoide': ruta_curva_sigmoide  
    }
    return resultados

@predResView.route("/pred-res", methods=["GET", "POST"])
def pred_res():
    modelo = shared_data.modelo
    X_test = shared_data.X_test
    y_test = shared_data.y_test

    boolean = modelo is not None and X_test is not None and y_test is not None
    resultados = None

    if boolean:
        flash("Podemos predecir tranquilamente", category="success")
    else:
        flash("No hay datos para predecir", category="error")

    if request.method == "POST":
        resultados = realizar_prediccion(modelo, X_test, y_test)

    return render_template("pred-res.html", show_button=boolean, resultados=resultados)
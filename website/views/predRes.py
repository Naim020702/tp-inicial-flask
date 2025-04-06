from flask import Blueprint, render_template, flash, request
from website.views.generar_matriz_confusion import generar_matriz_confusion
from website.views.generar_curva_sigmoide import generar_curva_sigmoide
from website import shared_data
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

predResView = Blueprint("predResView", __name__)

def realizar_prediccion(modelo, X_test, y_test):
    # Realizar predicciones
    y_pred = modelo.predict(X_test.drop(['id'], axis=1))

    # Calcular métricas de evaluacion
    precision = accuracy_score(y_test, y_pred)
    matriz_confusion = confusion_matrix(y_test, y_pred)
    reporte_clasificacion = classification_report(y_test, y_pred)

    # Generar y guardar la imagen de la matriz de confusión
    ruta_imagen = generar_matriz_confusion(matriz_confusion)

    # Generar y guardar la curva sigmoide
    ruta_curva_sigmoide = generar_curva_sigmoide(modelo, X_test.drop(['id'], axis=1))

    # Seleccionar una muestra de resultados reales y predichos
    ids = X_test['id'].tolist() # Obtener los ids de los candidatos
    muestra_resultados = list(zip(ids, y_test, y_pred)) # Combinar ids, resultados reales y predicciones

    # Diccionario con los resultados de la prediccion
    resultados = {
        'precision': precision,
        'matriz_confusion': matriz_confusion,
        'reporte_clasificacion': reporte_clasificacion,
        'ruta_imagen': ruta_imagen, 
        'ruta_curva_sigmoide': ruta_curva_sigmoide,
        'muestra_resultados': muestra_resultados  
    }
    return resultados

@predResView.route("/pred-res", methods=["GET", "POST"])
def pred_res():
    # Extrae el modelo y los datos de prueba de la informacion compartida
    modelo = shared_data.modelo
    X_test = shared_data.X_test
    y_test = shared_data.y_test

    # Si existen los elementos necesarios para predecir, se habilita el boton de predecir
    boolean = modelo is not None and X_test is not None and y_test is not None
    resultados = None

    if boolean:
        flash("Podemos predecir tranquilamente", category="success")
    else:
        flash("No hay datos para predecir", category="error")

    # Maneja la prediccion al presionar el boton
    if request.method == "POST":
        resultados = realizar_prediccion(modelo, X_test, y_test)
        shared_data.results = resultados # Almacenamos los datos de la prediccion en informacion compartida

    # Si ya existen resultados de prediccion, los mantenemos
    if shared_data.results is not None:
        resultados = shared_data.results

    # Avisamos al .html que se debe mostrar el boton para realizar la prediccion, ya que existe el modelo entrenado y los datos de prueba
    # Pasamos los resultados y candidatos para que se muestren en el .html
    return render_template("pred-res.html", show_button=boolean, resultados=resultados, candidatos=X_test)

# Ruta para info de un candidato especifico
@predResView.route("/candidato/<int:id>", methods=["GET"])
def ver_candidato(id):
    # Filtrar el candidato por ID en X_test
    candidato = shared_data.X_test[shared_data.X_test['id'] == id]

    if candidato.empty:
        flash("No se encontró información para este candidato.", category="error")
        return render_template("pred-res.html", show_button=True, resultados=None, candidatos=None)

    # Convertir la información del candidato a un diccionario para pasarla al template
    candidato_info = candidato.to_dict(orient="records")[0]

    return render_template("candidato.html", candidato=candidato_info)
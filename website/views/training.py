from flask import Blueprint, render_template, request, flash, current_app as app, send_file
import io
from website import shared_data
import os
from website import generate_data
import pandas as pd

# Importamos las librerias necesarias para el entrenamiento del modelo
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

trainingView = Blueprint("trainingView", __name__)

# Variable global para almacenar almacenar el DataFrame generado y para que pueda ser accedido desde multiples funciones
global_df = None

def carpeta_contiene_archivos():
    upload_folder = app.config.get("UPLOAD_FOLDER", "")
    if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
        archivos = os.listdir(upload_folder)  # Lista los archivos en la carpeta
        if archivos:  # Si la lista no está vacía
            return True
    return False

# Cada que se hace un GET a esta ruta se hacen las siguientes verificaciones
@trainingView.route("/training")
def previous_verification():
    global global_df
    class_distribution = None # Distribucion de clases inicializada
    # Si anteriormente ya se generaron o cargaron datos, establecer la misma tabla con su respectiva distribucion de clases
    if shared_data.already_generated:
        table = global_df.to_html(classes="table table-striped", index=False)
        class_distribution = global_df['apto'].value_counts().to_dict()
    # Si el usuario indicó una cantidad de registros adecuada...
    elif shared_data.received_registers is not None:
        flash(f"Cantidad de registros recibidos: {shared_data.received_registers}", category="info")
        global_df = generate_data.generar_csv(shared_data.received_registers) # Generar datos y almacenarlos en la var global
        shared_data.already_generated = True # Establecemos en informacion compartida que ya se generaron datos
        table = global_df.to_html(classes="table table-striped", index=False)
        class_distribution = global_df['apto'].value_counts().to_dict()  # Calcular distribución
    # Si el usuario cargo un archivo Csv de datos correctamente(La carpeta uploads no esta vacia)...
    elif carpeta_contiene_archivos():
        flash("La carpeta 'uploads' contiene archivos.", category="success")
        upload_folder = app.config.get("UPLOAD_FOLDER", "")
        archivos = os.listdir(upload_folder)
        if archivos:
            file_path = os.path.join(upload_folder, archivos[0])  # Toma el primer archivo
            global_df = pd.read_csv(file_path)  # Lee el archivo cargado y almacena los datos en la variable global
            table = global_df.to_html(classes="table table-striped", index=False)
            class_distribution = global_df['apto'].value_counts().to_dict()  # Calcular distribución
    # Si no habian datos ya generados, no se cargo un archivo ni se indico la cantidad de registros a generar...
    else:
        table = None
        flash("No hay datos disponibles para entrenar.", category="error")

    # Pasamos la tabla y distribucion de clases al .html si es que existen
    return render_template("training.html", table=table, class_distribution=class_distribution)

def entrenar_modelo(df):
    # Definimos variables categóricas y numéricas
    categorical_features = ['genero', 'habilidad', 'nivel_educativo']
    numeric_features = ['años_experiencia']

    # Preprocesador, que aplica OneHotEncoder a las categóricas
    # Un preprocesador es una transformación que se aplica a los datos antes de entrenar el modelo
    # OneHotEncoder convierte variables categóricas en variables dummy(0/1)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])

    # Crear pipeline
    # Un pipeline es una secuencia de pasos de procesamiento y modelado
    # Primero se aplica el preprocesador y luego se entrena el modelo de regresion logistica
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42))
    ])

    # Dividir datos
    X = df.drop(['apto'], axis=1) # Separamos las variables dependientes de las independientes
    y = df['apto'] # Variable dependiente
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) # Dividimos el dataset en entrenamiento y prueba

    # Entrenar modelo
    pipeline.fit(X_train.drop(['id'], axis=1), y_train)

    # Retorna el pipeline entrenado y los datos de prueba
    return pipeline, X_test, y_test

# Esta ruta es para se encarga de entrenar el modelo con los datos cargados o generados al presionar el boton
@trainingView.route("/training/train-model", methods=["POST"])
def btn_train_model():
    global global_df
    if request.method == "POST":
        if global_df is not None:
            modelo, X_test, y_test = entrenar_modelo(global_df)
            # Establece en la informacion compartida el modelo entrenado y los datos de prueba
            shared_data.modelo = modelo
            shared_data.X_test = X_test
            shared_data.y_test = y_test
            flash("El modelo se ha entrenado con los datos proporcionados...", category="success")
            
    return render_template("training.html", table=None)

# Esta ruta se encarga de descarga el archivo csv generado o cargado
@trainingView.route("/training/download-csv", methods=["GET"])
def download_csv():
    global global_df
    if global_df is not None:
        # Convertir el DataFrame a un archivo CSV en memoria
        csv_buffer = io.StringIO()
        global_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        # Enviar el archivo como una descarga
        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
            mimetype="text/csv",
            as_attachment=True,
            download_name="datos_generados.csv"
        )
    else:
        flash("No hay datos disponibles para descargar.", category="error")
        return render_template("training.html", table=None)
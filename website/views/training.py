from flask import Blueprint, render_template, request, flash, current_app as app, send_file
import io
from website import shared_data
import os
from website import generate_data
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

trainingView = Blueprint("trainingView", __name__)

global_df = None

def carpeta_contiene_archivos():
    upload_folder = app.config.get("UPLOAD_FOLDER", "")
    if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
        archivos = os.listdir(upload_folder)  # Lista los archivos en la carpeta
        if archivos:  # Si la lista no está vacía
            return True
    return False

@trainingView.route("/training")
def train():
    global global_df
    class_distribution = None
    if shared_data.already_generated:
        table = global_df.to_html(classes="table table-striped", index=False)
        class_distribution = global_df['apto'].value_counts().to_dict()
    elif shared_data.received_registers is not None:
        flash(f"Cantidad de registros recibidos: {shared_data.received_registers}", category="info")
        global_df = generate_data.generar_csv(shared_data.received_registers)
        shared_data.already_generated = True
        table = global_df.to_html(classes="table table-striped", index=False)
        class_distribution = global_df['apto'].value_counts().to_dict()  # Calcular distribución
    elif carpeta_contiene_archivos():
        flash("La carpeta 'uploads' contiene archivos.", category="success")
        upload_folder = app.config.get("UPLOAD_FOLDER", "")
        archivos = os.listdir(upload_folder)
        if archivos:
            file_path = os.path.join(upload_folder, archivos[0])  # Toma el primer archivo
            global_df = pd.read_csv(file_path)  # Guarda el DataFrame en la variable global
            table = global_df.to_html(classes="table table-striped", index=False)
            class_distribution = global_df['apto'].value_counts().to_dict()  # Calcular distribución
    else:
        table = None
        flash("No hay datos disponibles para entrenar.", category="error")

    return render_template("training.html", table=table, class_distribution=class_distribution)

def entrenar_modelo(df):
    categorical_features = ['genero', 'habilidad', 'nivel_educativo']
    numeric_features = ['años_experiencia']

    # Preprocesador
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])

    # Crear pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42))
    ])

    # Dividir datos
    X = df.drop(['apto'], axis=1)
    y = df['apto']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Entrenar modelo
    pipeline.fit(X_train.drop(['id'], axis=1), y_train)

    return pipeline, X_test, y_test

@trainingView.route("/training/train-model", methods=["POST"])
def train_model():
    global global_df
    if request.method == "POST":
        flash("El modelo se ha entrenado con los datos proporcionados...", category="success")
        if global_df is not None:
            modelo, X_test, y_test = entrenar_modelo(global_df)
            shared_data.modelo = modelo
            shared_data.X_test = X_test
            shared_data.y_test = y_test
            print("Modelo entrenado con exito")
            
    return render_template("training.html", table=None)

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
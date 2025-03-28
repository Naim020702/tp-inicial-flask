from flask import Blueprint, render_template, request, flash, current_app as app
from website import shared_data
import os
from website import generate_data
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

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
    if shared_data.received_registers is not None:
        flash(f"Cantidad de registros recibidos: {shared_data.received_registers}", category="info")
        #GENERAR EL DATASET CON LA CANT DE MUESTRAS QUE INDICO EL USUARIO
        # df = generate_data.generar_csv(shared_data.received_registers)
        global_df = generate_data.generar_csv(shared_data.received_registers)
        # table = df.to_html(classes="table table-striped", index=False)
        table = global_df.to_html(classes="table table-striped", index=False)
        # print(df)
        print(global_df)
    elif carpeta_contiene_archivos():
        flash("La carpeta 'uploads' contiene archivos.", category="success")
        #LEVANTAR EL DATASET CARGADO POR USUARIO
        upload_folder = app.config.get("UPLOAD_FOLDER", "")
        archivos = os.listdir(upload_folder)
        if archivos:
            file_path = os.path.join(upload_folder, archivos[0])  # Toma el primer archivo
            # df = pd.read_csv(file_path)
            global_df = pd.read_csv(file_path)  # Guarda el DataFrame en la variable global
            # table = df.to_html(classes="table table-striped", index=False) 
            table = global_df.to_html(classes="table table-striped", index=False)
    else:
        table = None
        flash("No hay datos disponibles para entrenar.", category="error")

    return render_template("training.html", table=table)

def entrenar_modelo(df):
    # Preparar los datos para el entrenamiento
    X = df[['Años_Experiencia', 'Nivel_Educativo', 'Habilidad_Python', 'Habilidad_Java', 'Habilidad_SQL']]
    y = df['Apto']

    # Convertir variables categóricas
    columnas_categoricas = ['Nivel_Educativo']
    transformador = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), columnas_categoricas)
        ],
        remainder='passthrough'
    )
    X = transformador.fit_transform(X)

    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    modelo = LogisticRegression()
    modelo.fit(X_train, y_train)

    # Devolver el modelo entrenado, los datos de prueba y el transformador
    return modelo, X_test, y_test

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
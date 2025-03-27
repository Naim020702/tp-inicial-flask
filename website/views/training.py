from flask import Blueprint, render_template, request, flash, current_app as app
from website import shared_data
import os
from website import generate_data
import pandas as pd

trainingView = Blueprint("trainingView", __name__)

def carpeta_contiene_archivos():
    upload_folder = app.config.get("UPLOAD_FOLDER", "")
    if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
        archivos = os.listdir(upload_folder)  # Lista los archivos en la carpeta
        if archivos:  # Si la lista no está vacía
            return True
    return False

@trainingView.route("/training")
def train():
    if shared_data.received_registers is not None:
        flash(f"Cantidad de registros recibidos: {shared_data.received_registers}", category="info")
        #GENERAR EL DATASET CON LA CANT DE MUESTRAS QUE INDICO EL USUARIO
        df = generate_data.generar_csv(shared_data.received_registers)
        table = df.to_html(classes="table table-striped", index=False)
        print(df)
    elif carpeta_contiene_archivos():
        flash("La carpeta 'uploads' contiene archivos.", category="success")
        #LEVANTAR EL DATASET CARGADO POR USUARIO
        upload_folder = app.config.get("UPLOAD_FOLDER", "")
        archivos = os.listdir(upload_folder)
        if archivos:
            file_path = os.path.join(upload_folder, archivos[0])  # Toma el primer archivo
            df = pd.read_csv(file_path)
            table = df.to_html(classes="table table-striped", index=False) 
    else:
        table = None
        flash("No hay datos disponibles para entrenar.", category="error")


    return render_template("training.html", table=table)
# request para manejar las peticiones HTTP
# Flash para mostrar mensajes al usuario
# os para manejar el sistema de archivos
# shared_data para manejar datos compartido entre vistas
# pandas para leer datos Csv
from flask import Blueprint, render_template, request, current_app as app, flash
import os
from website import shared_data
import pandas as pd

# Crea la vista
dataGenView = Blueprint("dataGenView", __name__)

# Esta ruta puede aceptar tanto GET como POST
@dataGenView.route("/data-gen", methods=["GET", "POST"])
def data_gen():
    # Si el usuario hace un POST, se procesan los datos que brindó
    if request.method == "POST":
        # Reiniciar la informacion compartida por si quedó de un procesamiento anterior
        shared_data.modelo = None
        shared_data.X_test = None
        shared_data.y_test = None
        shared_data.already_generated = None
        shared_data.results = None
        shared_data.received_registers = None

        # Borrar lo que haya en la carpeta uploads
        upload_folder = app.config.get("UPLOAD_FOLDER", "")
        if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
            archivos = os.listdir(upload_folder)
            if archivos:
                for archivo in archivos:
                    os.remove(os.path.join(upload_folder, archivo))

        # Guarda el archivo CSV o la cantidad de registros a generar, extraidos de la peticion
        archivo = request.files.get("archivo_csv")
        cant_registers = request.form.get("cant_registers")

        # Caso 1: Procesar archivo CSV si se envió
        if archivo and archivo.filename != '':
            # Es .csv?
            if archivo.filename.endswith('.csv'):
                try:
                    # Guardar el archivo en la carpeta de uploads
                    filename = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
                    archivo.save(filename)

                    # Procesar el archivo CSV
                    datos = pd.read_csv(filename)

                    # Verificar si contiene las columnas adecuadas
                    columnas_esperadas = {"id", "genero", "años_experiencia", "habilidad", "nivel_educativo", "probabilidad_apto", "apto"}
                    columnas_archivo = set(datos.columns)

                    # Si las columnas esperadas no coinciden con las que que tiene el archivo, es eliminado y se muestra msj de error
                    if not columnas_esperadas.issubset(columnas_archivo):
                        flash(f"El archivo no contiene las columnas adecuadas. Se esperaban: {', '.join(columnas_esperadas)}", category="error")
                        os.remove(filename)
                    else:
                        flash(f"Archivo recibido con {len(datos)} registros", category="success")
                except Exception as e:
                    flash(f"Error al procesar el archivo: {str(e)}", category="error")
            else:
                flash("Formato de archivo no válido. Solo se permiten archivos .csv", category="error")

        # Caso 2: Procesar cantidad de muestras si se ingresó
        elif cant_registers:
            try:
                cant_registers = int(cant_registers)
                # Si la cantidad de muestras es menor a 50, mostramos un msj de error
                if cant_registers < 50:
                    flash("La cantidad de muestras debe ser al menos 50", category="error")
                else:
                    # Establecemos en la informacion compartida la cantidad de registros a generar, informacion que será levantada por training.py
                    shared_data.received_registers = cant_registers
                    flash(f"Se generaron {cant_registers} registros correctamente", category="success")
            except ValueError:
                flash("La cantidad de muestras debe ser un número válido", category="error")

        # Caso 3: Ninguna opción fue seleccionada
        else:
            flash("Debe seleccionar un archivo CSV o ingresar la cantidad de muestras a generar", category="error")

    return render_template("data-gen.html")
from flask import Blueprint, render_template, request, current_app as app, flash
import os
from website import shared_data

dataGenView = Blueprint("dataGenView", __name__)

@dataGenView.route("/data-gen", methods=["GET", "POST"])
def data_gen():
    if request.method == "POST":
        shared_data.modelo = None
        shared_data.X_test = None
        shared_data.y_test = None

        # borrar lo que haya en la carpeta uploads
        upload_folder = app.config.get("UPLOAD_FOLDER", "")
        if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
            archivos = os.listdir(upload_folder)
            if archivos:
                for archivo in archivos:
                    os.remove(os.path.join(upload_folder, archivo))

        #borrar la cantidad de registros recibidos
        shared_data.received_registers = None

        archivo = request.files.get("archivo_csv")
        cant_registers = request.form.get("cant_registers")

        # Caso 1: Procesar archivo CSV si se envió
        if archivo and archivo.filename != '':
            if archivo.filename.endswith('.csv'):
                try:
                    # Guardar el archivo
                    filename = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
                    archivo.save(filename)

                    # Procesar el archivo CSV
                    import pandas as pd
                    datos = pd.read_csv(filename)

                    flash(f"Archivo recibido con {len(datos)} registros", category="success")
                except Exception as e:
                    flash(f"Error al procesar el archivo: {str(e)}", category="error")
            else:
                flash("Formato de archivo no válido. Solo se permiten archivos .csv", category="error")

        # Caso 2: Procesar cantidad de muestras si se ingresó
        elif cant_registers:
            try:
                cant_registers = int(cant_registers)
                if cant_registers < 50:
                    flash("La cantidad de muestras debe ser al menos 50", category="error")
                else:
                    # Aquí puedes implementar la lógica para generar datos ficticios
                    shared_data.received_registers = cant_registers
                    # print(shared_data.received_registers)
                    flash(f"Se generaron {cant_registers} registros correctamente", category="success")
            except ValueError:
                flash("La cantidad de muestras debe ser un número válido", category="error")

        # Caso 3: Ninguna opción fue seleccionada
        else:
            flash("Debe seleccionar un archivo CSV o ingresar la cantidad de muestras a generar", category="error")

    return render_template("data-gen.html")
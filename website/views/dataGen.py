from flask import Blueprint, render_template, request, current_app as app, flash
import os

dataGen = Blueprint("dataGen", __name__)

@dataGen.route("/data-gen", methods=["GET", "POST"])
def data_gen():
    if request.method == "POST":
        # if "archivo_csv" in request.files:
        #     archivo = request.files["archivo_csv"]

        #     if archivo.filename == '':
        #         # return 'Nombre de archivo vacío', 400
        #         flash("Nombre de archivo vacio", category="error")
        #         # pass
        
        #     if archivo and archivo.filename.endswith('.csv'):
        #         # Guardar el archivo
        #         filename = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
        #         archivo.save(filename)

        #         import pandas as pd
        #         datos = pd.read_csv(filename)

        #         # return f"Archivo recibido con {len(datos)} registros"
        #         flash(f"Archivo recibido con {len(datos)} registros", category="success")
        #         # pass
        #     else:
        #         # return "Formato de arhivo no valido", 400
        #         flash("Formato de archivo no valido", category="error")
        #         # pass
    
        # cant_registers = request.form.get("cant_registers")
        # if cant_registers:
        #     try:
        #         cant_registers = int(cant_registers)
        #         if cant_registers < 50:
        #             # return "La cantidad de muestras debe ser al menos 50", 400
        #             flash("La cantidad de muestras debe ser al menos 50", category="error")
        #             # pass
        #         else:
        #             # return f"Se generaron {cant_registers} registros"
        #             flash(f"Se generaron {cant_registers} registros", category="success")
        #     except ValueError:
        #         # return "La cantidad de muestras debe ser un numero valido", 400
        #         flash("La cantidad de muestras debe ser un numero valido", category="error")
        #         # pass
        # else:
        #     # return "Debe seleccionar un archivo csv o ingresar la cantidad de muestras a generar"
        #     flash("Debe seleccionar un archivo csv o ingresar la cantidad de muestras a generar", category="error")
        #     # pass

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
                    flash(f"Se generaron {cant_registers} registros correctamente", category="success")
            except ValueError:
                flash("La cantidad de muestras debe ser un número válido", category="error")

        # Caso 3: Ninguna opción fue seleccionada
        else:
            flash("Debe seleccionar un archivo CSV o ingresar la cantidad de muestras a generar", category="error")

    return render_template("data-gen.html")
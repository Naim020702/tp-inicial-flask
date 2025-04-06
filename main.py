# Importa la funcion para crear la aplicacion de Flask
from website import create_app

# Creacion de la aplicacion, ya implementada en el archivo __init__.py
app = create_app()

# Si este archivo es ejecutado directamente, se inicia la aplicacion
if __name__ == "__main__":
    app.run(debug=True)
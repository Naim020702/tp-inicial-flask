import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def generar_matriz_confusion(matriz_confusion):
    """Genera y guarda una imagen de la matriz de confusión con colores personalizados y etiquetas debajo de los números."""
    plt.figure(figsize=(6, 6))

    # Colores para cada cuadrante
    colores = np.array([
        ["#32cd32", "#ff6347"],  # Verdaderos Positivos en verde y Falsos Positivos en rojo
        ["#ffeb3b", "#006400"]   # Falsos Negativos en amarillo y Verdaderos Negativos en verde oscuro
    ])

    # Rellenar los cuadrantes con los colores correspondientes
    for i in range(matriz_confusion.shape[0]):
        for j in range(matriz_confusion.shape[1]):
            plt.fill_between([j, j + 1], [i, i], [i + 1, i + 1], color=colores[i, j])  # Colorear cuadrante
            # Colocar el valor de la matriz en su correspondiente cuadrante
            plt.text(j + 0.5, i + 0.5, str(matriz_confusion[i, j]), ha='center', va='center', 
                    color='black', fontsize=12, fontweight='bold')

    # Cambiar las etiquetas de los cuadrantes según lo solicitado y colocarlas debajo de los números
    etiquetas = np.array([
        ["Verdaderos Positivos", "Falsos Positivos"],  # Primera fila
        ["Falsos Negativos", "Verdaderos Negativos"]   # Segunda fila
    ])

    # Colocar las etiquetas debajo de los números dentro de los cuadrantes
    for i in range(etiquetas.shape[0]):
        for j in range(etiquetas.shape[1]):
            plt.text(j + 0.5, i + 0.2, etiquetas[i, j], ha='center', va='center', fontsize=9, color='black')

    # Eliminar los ticks de los ejes
    plt.xticks([])
    plt.yticks([])
    plt.title('Matriz de Confusión')
    plt.grid(False)

    # Guardar el gráfico
    ruta_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
    ruta_static = os.path.abspath(ruta_static)  # Normaliza la ruta absoluta
    if not os.path.exists(ruta_static):
        os.makedirs(ruta_static)

    ruta_imagen = os.path.join(ruta_static, 'matriz_confusion.png')
    plt.savefig(ruta_imagen)
    plt.close()

    return ruta_imagen

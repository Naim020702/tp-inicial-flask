import numpy as np
import matplotlib.pyplot as plt
import os

def generar_curva_sigmoide(modelo, X_test):
    # Crear la curva sigmoide ideal
    plt.figure(figsize=(6, 6))
    x_range = np.linspace(-10, 10, 100)
    sigmoide = 1 / (1 + np.exp(-x_range))  # Curva sigmoide ideal
    plt.plot(x_range, sigmoide, color='green', lw=2)

    # Obtener las probabilidades predichas (solo la clase positiva)
    y_prob = modelo.predict_proba(X_test)[:, 1]

    # Obtener el valor de entrada ponderado (antes de la función sigmoide)
    valor_entrada_ponderado = modelo.named_steps['preprocessor'].transform(X_test)
    
    # Si el modelo tiene coef_ e intercept_ (como regresión logística), calculamos la entrada ponderada
    if hasattr(modelo.named_steps['classifier'], 'coef_') and hasattr(modelo.named_steps['classifier'], 'intercept_'):
        # Para modelos lineales (como regresión logística), calculamos la entrada ponderada
        valor_entrada_ponderado = np.dot(valor_entrada_ponderado, modelo.named_steps['classifier'].coef_.T) + modelo.named_steps['classifier'].intercept_
        
        # Aplicar la función sigmoide a la entrada ponderada para obtener las probabilidades predichas
        y_pred_sigmoide = 1 / (1 + np.exp(-valor_entrada_ponderado))
        
        # Graficar los puntos en la curva sigmoide utilizando el valor de entrada ponderado
        plt.scatter(valor_entrada_ponderado, y_pred_sigmoide, color='red', label='Predicciones')

    # Configuración de la gráfica
    plt.title('Curva de Probabilidad (Sigmoide)')
    plt.xlabel('Valor de entrada ponderado')
    plt.ylabel('Probabilidad predicha de ser Apto')
    plt.legend()

    # Guardar la curva sigmoide
    ruta_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')   
    ruta_static = os.path.abspath(ruta_static)  # Normaliza la ruta absoluta

    # Crear el directorio si no existe
    if not os.path.exists(ruta_static):
        os.makedirs(ruta_static)
    ruta_sigmoide = os.path.join(ruta_static, 'curva_sigmoide.png')

    # Guardar la imagen
    plt.savefig(ruta_sigmoide)
    plt.close()

    return ruta_sigmoide

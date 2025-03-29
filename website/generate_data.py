import numpy as np
import pandas as pd
import random

# # Calculo la probabilidad de ser "Apto"
# def calcular_probabilidad(años_experiencia, nivel_educativo, habilidad_python, habilidad_java, habilidad_sql):
#     # Asigno pesos a cada característica
#     peso_experiencia = 0.1
#     peso_educativo = {'Primario': 0.1, 'Secundario': 0.3, 'Universitario': 0.5}
#     peso_python = 0.3
#     peso_java = 0.2
#     peso_sql = 0.2

#     # Calculo puntuación
#     puntuacion = (
#         peso_experiencia * años_experiencia +
#         peso_educativo[nivel_educativo] +
#         peso_python * habilidad_python +
#         peso_java * habilidad_java +
#         peso_sql * habilidad_sql
#         )

#     # Convierto la puntuación en una probabilidad usando la función sigmoide
#     probabilidad = 1 / (1 + np.exp(-puntuacion))
#     return probabilidad

# def generar_csv(n_registros):
#     np.random.seed(42)  # Datos ficticios, reproducible

#     n_candidatos = n_registros  # Cantidad de muestras

#     # Genero datos aleatorios
#     id_candidato = np.arange(1, n_candidatos + 1)  # ID único para cada candidato
#     genero = np.random.choice(['Masculino', 'Femenino'], n_candidatos)  # Género (no influye en la clasificación)
#     años_experiencia = np.random.randint(0, 10, n_candidatos)
#     nivel_educativo = np.random.choice(['Primario', 'Secundario', 'Universitario'], n_candidatos)
#     habilidad_python = np.random.randint(0, 2, n_candidatos)  # 0: No, 1: Sí
#     habilidad_java = np.random.randint(0, 2, n_candidatos)  # 0: No, 1: Sí
#     habilidad_sql = np.random.randint(0, 2, n_candidatos)  # 0: No, 1: Sí

#     # Calculo probabilidades para cada candidato
#     probabilidades = [
#         calcular_probabilidad(años_exp, nivel_edu, python, java, sql)
#         for años_exp, nivel_edu, python, java, sql in zip(años_experiencia, nivel_educativo, habilidad_python, habilidad_java, habilidad_sql)
#     ]

#     # Genero la etiqueta "Apto" de manera aleatoria según las probabilidades
#     apto = np.random.binomial(1, probabilidades)

#     # Creo el DataFrame
#     data = {
#         'ID': id_candidato,
#         'Genero': genero,
#         'Años_Experiencia': años_experiencia,
#         'Nivel_Educativo': nivel_educativo,
#         'Habilidad_Python': habilidad_python,
#         'Habilidad_Java': habilidad_java,
#         'Habilidad_SQL': habilidad_sql,
#         'Probabilidad_Apto': probabilidades,
#         'Apto': apto
#     }

#     df = pd.DataFrame(data)
#     return df

def generar_csv(num_candidatos=100):
    """
    Genera un DataFrame de candidatos con información personal y calcula su probabilidad de ser aptos.
    
    Args:
        num_candidatos (int): Número de candidatos a generar. Por defecto 100.
    
    Returns:
        pd.DataFrame: DataFrame con información de candidatos y su probabilidad de ser aptos.
    """
    # Listas de posibles valores para cada categoría
    generos = ['Masculino', 'Femenino']
    habilidades = ['Python', 'JavaScript', 'SQL']
    niveles_educativos = ['Primario', 'Secundario', 'Universitario']
    
    # Generar datos aleatorios para cada columna
    ids = range(1, num_candidatos + 1)
    generos_rand = [random.choice(generos) for _ in range(num_candidatos)]
    exp_rand = [random.randint(0, 10) for _ in range(num_candidatos)]
    habilidades_rand = [random.choice(habilidades) for _ in range(num_candidatos)]
    educacion_rand = [random.choice(niveles_educativos) for _ in range(num_candidatos)]
    
    # Crear DataFrame
    df = pd.DataFrame({
        'id': ids,
        'genero': generos_rand,
        'años_experiencia': exp_rand,
        'habilidad': habilidades_rand,
        'nivel_educativo': educacion_rand
    })
    
    # Función para calcular probabilidad de ser apto
    def calcular_probabilidad(row):
        probabilidad = 0.3  # Probabilidad base
        
        # Aumentar probabilidad según criterios
        if row['habilidad'] == 'Python':
            probabilidad += 0.2
        if row['nivel_educativo'] == 'Universitario':
            probabilidad += 0.25
        if row['años_experiencia'] >= 3:
            probabilidad += 0.15 + min(row['años_experiencia'] / 20, 0.1)  # Máximo 10% adicional por experiencia
        
        # Ajustar para que no supere 1
        probabilidad = min(probabilidad, 0.95)  # Nunca 100% seguro
        
        # Pequeña probabilidad incluso para candidatos con menos cualificaciones
        probabilidad = max(probabilidad, 0.05)
        
        return round(probabilidad, 2)
    
    # Aplicar la función y determinar si es apto
    df['probabilidad_apto'] = df.apply(calcular_probabilidad, axis=1)
    df['apto'] = df['probabilidad_apto'].apply(lambda x: 'Sí' if x >= 0.7 else 'No')
    
    return df
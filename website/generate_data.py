import pandas as pd
import random

# Funcion para generar un csv con datos aleatorios de candidatos
def generar_csv(num_candidatos=100):
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
    
    # Función para calcular probabilidad de ser apto, toma los valores de cada fila(habilidad, nivel educ y años exp)
    # Esto es para cada candidato
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
        
        # Redondear a dos decimales
        return round(probabilidad, 2)
    
    # Aplicar la función y determinar si es apto
    df['probabilidad_apto'] = df.apply(calcular_probabilidad, axis=1)
    df['apto'] = df['probabilidad_apto'].apply(lambda x: 'Sí' if x >= 0.7 else 'No')
    
    # Retorna el DataFrame, al cual se le agrego la columna de apto y probabilidad
    return df
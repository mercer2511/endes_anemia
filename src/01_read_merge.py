"""
01_read_merge.py
Lee los cuatro CSV cruciales, depura y genera un Parquet limpio
para el análisis de regresión ordinal.
"""
import pandas as pd

# Ruta a la carpeta donde se encuentran los CSV
DATA = "../data/"


def read_minimal():
    """
    Lee los archivos CSV esenciales y fusiona la información.
    Retorna un DataFrame combinado.
    """
    # --- RECH6: Datos del niño ---
    # Se leen las columnas esenciales:
    # HHID: Identificador del hogar.
    # HC0: Número de orden del niño.
    # HC1: Edad en meses del niño.
    # HC27: Sexo del niño.
    # HC57: Nivel de anemia (1=grave, 2=moderada, 3=leve, 4=sin anemia).
    # HC60: Número de orden de la madre en el hogar (para el enlace con RECH1).
    rech6 = pd.read_csv(DATA + "RECH6_2023.csv",
                        usecols=['HHID', 'HC0', 'HC1', 'HC27', 'HC57', 'HC60'])

    # --- RECH0: Datos del hogar / diseño muestral ---
    # Se obtienen el cluster, estrato, factor de ponderación, etc.
    rech0 = pd.read_csv(DATA + "RECH0_2023.csv",
                        usecols=['HHID', 'HV001', 'HV022', 'HV005'])

    # --- RECH23: Índice de riqueza del hogar ---
    # Se extraen HV270 (índice/quintil de riqueza) y HV271 (puntaje continuo)
    rech23 = pd.read_csv(DATA + "RECH23_2023.csv",
                         usecols=['HHID', 'HV270', 'HV271'])

    # --- RECH1: Datos de la madre y otras características ---
    # Se utilizan para obtener información de la madre (edad, educación)
    rech1 = pd.read_csv(DATA + "RECH1_2023.csv",
                        usecols=['HHID', 'HVIDX', 'HV104', 'HV105', 'HV106', 'HV109'])

    # --- Fusionar módulos ---
    # Primero se une RECH6, RECH0 y RECH23 según HHID.
    df = rech6.merge(rech0, on='HHID', how='left') \
        .merge(rech23, on='HHID', how='left')

    # Renombrar en RECH1 para que se alinee la columna que identifica la línea de la madre
    madre = rech1.rename(columns={
        'HVIDX': 'HC60',  # Para unir con la información de RECH6 (columna HC60)
        'HV104': 'sexo_madre',
        'HV105': 'edad_madre',
        'HV106': 'edu_sup',  # Nivel educativo superior (o similar)
        'HV109': 'edu_det'  # Nivel educativo detallado, si es necesario
    })
    # Unir datos de la madre al dataframe principal usando HHID y HC60
    df = df.merge(madre[['HHID', 'HC60', 'edad_madre', 'edu_sup', 'edu_det']],
                  on=['HHID', 'HC60'], how='left')

    return df


def clean(df):
    # Filtrar niños entre 6 y 59 meses usando la columna 'HC1'
    df = df[df['HC1'].between(6, 59) & df['HC57'].isin([1, 2, 3, 4])]

    # Convertir HV270 a numérico (índice de riqueza)
    df['HV270'] = pd.to_numeric(df['HV270'], errors='coerce')

    # Calcular el peso de la muestra: dividir HV005 entre 1,000,000
    df['peso'] = df['HV005'] / 1_000_000

    # Utilizar directamente HV270 como quintil (ya clasificado en 1 a 5)
    df['quintil'] = df['HV270'].astype(int)

    # Recodificar el sexo del niño: asumiendo 1 = niño, 2 = niña → 0 = niño, 1 = niña
    df['sexo_nino'] = df['HC27'].replace({1: 0, 2: 1})

    # Crear variable de anemia binaria: 1 = anémico (HC57 distinto de 4), 0 = sin anemia
    df['anemia_bin'] = (df['HC57'] != 4).astype(int)

    return df


if __name__ == "__main__":
    df = clean(read_minimal())
    df.to_parquet("../outputs/anemia_clean.parquet")
    print("Archivo guardado: anemia_clean.parquet")
    print("Número total de registros:", len(df))

print(df['HV270'].describe())
print(df['HV270'].value_counts().sort_index())
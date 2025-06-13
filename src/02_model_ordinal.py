"""
02_model_ordinal.py
Ajusta una regresión ordinal logit con la variable de anemia (HC57)
y guarda el resumen en outputs/modelo_ordinal.txt
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel

# Cargar el dataset limpio generado en el paso anterior
df = pd.read_parquet("../outputs/anemia_clean.parquet")

# Agregar constante para el modelo (aunque OrderedModel no la requiere, la agregamos
# y luego la eliminaremos de X)
df['const'] = 1  # Intercepto

# --- Seleccionar y preparar variables predictoras (X) y la variable respuesta (y)
# Usar 'HC1' para la edad del niño, y otras variables según lo definido.
X = pd.get_dummies(df[['const', 'quintil', 'HC1', 'sexo_nino', 'edad_madre', 'edu_sup']], drop_first=True)

y = df['HC57']

# --- Manejo de datos faltantes en las variables predictoras

missing_count = X.isnull().sum().sum()
print("Número total de valores faltantes en X:", missing_count)

mask = X.isnull().any(axis=1)
if mask.sum() > 0:
    print(f"Eliminando {mask.sum()} filas con datos faltantes en X")
    X = X[~mask]
    y = y[~mask]

if np.any(np.isinf(X)):
    print("Se encontraron valores infinitos en X. Reemplazándolos por nan y eliminando filas correspondientes.")
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    mask = X.isnull().any(axis=1)
    X = X[~mask]
    y = y[~mask]

# --- Eliminar la constante en X ya que OrderedModel no la permite.
if 'const' in X.columns:
    X = X.drop('const', axis=1)

# --- Definir el modelo ordinal logit (usando pesos)
model = OrderedModel(
    y, X, distr='logit', weights=df.loc[X.index, 'peso']
)

# Ajustar el modelo utilizando el método 'bfgs'
res = model.fit(method='bfgs', disp=0)

# Guardar el resumen del modelo en un archivo de texto
with open("../outputs/modelo_ordinal.txt", "w") as f:
    f.write(res.summary().as_text())

print(res.summary())
print("\nOdds-ratios aproximados:")
print(np.exp(res.params).round(3))
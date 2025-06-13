# Documento Metodológico

## 1. Sección de Datos

**Fuentes y Contenido de los Módulos:**

- **RECH6_2023.csv – Datos del Niño**  
  - **Contenido:**  
    Este módulo contiene la información de los niños encuestados, incluyendo variables clave para el análisis de la anemia.  
  - **Variables relevantes:**  
    - `HHID`: Identificador del hogar, clave para la fusión con otros módulos.  
    - `HC0`: Número de orden del niño.  
    - `HC1`: Edad en meses del niño.  
    - `HC27`: Género del niño (usualmente codificado, por ejemplo, 1 = niño, 2 = niña).  
    - `HC57`: Indicador ordinal del nivel de anemia (codificado, por ejemplo, 1 = anemia grave, 2 = moderada, 3 = leve, 4 = sin anemia).  
    - `HC60`: Número de orden de la madre en el hogar, usado para enlazar con el módulo RECH1.  

- **RECH0_2023.csv – Datos del Hogar y Diseño Muestral**  
  - **Contenido:**  
    Proporciona información sobre la estructura del hogar, variables de diseño muestral y ponderadores.  
  - **Variables relevantes:**  
    - `HHID`: Identificador del hogar.  
    - `HV001`: Código del conglomerado o cluster.  
    - `HV022`: Estrato muestral del hogar.  
    - `HV005`: Factor de ponderación, utilizado para ajustar los análisis a la distribución de la población (normalmente se aplica una transformación, por ejemplo, dividiéndolo entre 1,000,000).  

- **RECH23_2023.csv – Información de la Vivienda e Índice de Riqueza**  
  - **Contenido:**  
    Contiene variables que describen la vivienda y los bienes del hogar, las cuales se han utilizado para construir el índice de bienestar o riqueza.  
  - **Variables relevantes:**  
    - `HHID`: Identificador del hogar.  
    - `HV270`: Índice de riqueza, categorizado en rangos enteros (1 a 5), que sirve para generar la variable `quintil`.  
    - `HV271`: Puntaje continuo del índice de riqueza (opcional para análisis alternativos).

- **RECH1_2023.csv – Datos del Roster Familiar (Madre)**  
  - **Contenido:**  
    Este módulo contiene la información vinculada a las madres, vinculada a los niños a través del identificador `HC60`.  
  - **Variables relevantes:**  
    - `HHID`: Identificador del hogar.  
    - `HVIDX`: Se renombra a `HC60` para unir con RECH6.  
    - `HV104`: Género de la madre (no requerido para este análisis, pero disponible).  
    - `HV105`: Edad de la madre, utilizada para agregar información demográfica.  
    - `HV106`: Nivel educativo (se renombra usualmente a `edu_sup`), que refleja la capacidad educativa.  
    - `HV109`: Otra medida del nivel educativo, disponible para análisis complementarios.

---

## 2. Procedimiento Analítico

**A. Lógica Detrás de la Limpieza de Datos y Manejo de Missing Values:**

- **Fusión de Módulos:**  
  Los diferentes módulos se unen utilizando la llave `HHID`. Además, para unir datos de la madre y el niño se utiliza la variable `HC60` (originalmente `HVIDX` en RECH1, renombrada para hacer la unión).
  
- **Filtrado de Registros:**  
  Se filtran los registros para conservar únicamente aquellos niños en el rango de edad de 6 a 59 meses, y se excluyen registros con valores inválidos en la variable de anemia (`HC57` fuera del rango {1,2,3,4}).

- **Conversión de Variables:**  
  Se realizan transformaciones clave como:
  - Convertir `HV270` a numérico y generar la variable `quintil` directamente a partir de ella (dado que ya se encuentra categorizada de 1 a 5).
  - Calcular el factor de ponderación (`peso`) a partir de `HV005` (dividido por 1,000,000).
  - Recodificar el sexo del niño, por ejemplo, convirtiendo `HC27` a una variable binaria (`sexo_nino`) donde 0 representa a los niños y 1 a las niñas.

- **Manejo de Missing Values e Infinitos:**  
  Se identifican y eliminan las filas que contienen valores faltantes o infinitos en las variables clave utilizadas para el modelo, asegurando así la integridad de la matriz de variables predictoras.

**B. Configuración de Variables:**

- **Variable Respuesta (y):**  
  `HC57`, la variable ordinal que clasifica la anemia en 4 categorías (de más grave a sin anemia).

- **Variables Predictoras (X):**  
  - `quintil`: Indicador del nivel de bienestar.
  - `HC1`: Edad en meses.
  - `sexo_nino`: Sexo del niño (codificado como 0/1).
  - `edad_madre`: Edad de la madre.
  - `edu_sup`: Nivel educativo de la madre.

- **Variables en el Modelo:**  
  Uso de dummies para variables categóricas y aplicación de técnicas para prevenir problemas de multicolinealidad (por ejemplo, al usar `pd.get_dummies` con `drop_first=True`).

**C. Selección y Ajuste del Modelo Ordenal:**

- **Razonamiento del Modelo:**  
  Se utiliza un **modelo de regresión ordinal logit** (con `OrderedModel` de statsmodels) para aprovechar la naturaleza ordinal de la variable respuesta `HC57`. La elección de este modelo permite interpretar los parámetros en términos de acumulación de probabilidad y definir umbrales que separan las categorías.

- **Uso de Ponderadores:**  
  Al incluir la variable `peso` (derivada de `HV005`), se incorporan los ajustes por diseño muestral, garantizando que las inferencias sean representativas de la población.

- **Procedimiento de Ajuste:**  
  Se utiliza el método `bfgs` para la optimización y se procede a interpretar tanto los coeficientes como los parámetros de corte (thresholds) del modelo.

---

## 3. Interpretación y Validación de Resultados

**Interpretación de Odds Ratios y Significancia Estadística:**

- **Odds Ratios:**  
  Los coeficientes del modelo se transforman en odds ratios mediante la función exponencial. Por ejemplo, un odds ratio mayor que 1 en la variable `quintil` sugiere que, conforme aumenta el nivel de bienestar (pasando de un quintil inferior a superior), incrementa la probabilidad de que el niño esté en una categoría de anemia menos grave.

- **Significancia Estadística:**  
  Se examinan los p-values para determinar cuáles variables son estadísticamente significativas. En el output, los valores p menores a 0.05 indican que la relación observada no es producto del azar.
  
- **Parámetros de Corte (Thresholds):**  
  Los umbrales (por ejemplo, `1/2`, `2/3`, `3/4`) indican los puntos donde la probabilidad acumulada cambia de una categoría a otra. Estos se utilizan para definir la estructura ordinal de la variable respuesta.

**Diagnósticos del Modelo:**

- **Análisis de Residuales:**  
  Es importante evaluar si los residuales del modelo presentan patrones sistemáticos que puedan indicar problemas de ajuste. Una inspección visual mediante gráficos de residuales versus valores predichos puede ayudar a detectar desviaciones de los supuestos del modelo.

- **Validación y Robustez:**  
  - Se pueden realizar análisis de sensibilidad –por ejemplo, modificando la selección de covariables o utilizando una regresión logística binaria alternativa– para confirmar la robustez de los efectos observados.
  - Si es posible, implementar validación cruzada (cross-validation) cuantifica la estabilidad del modelo en diferentes particiones del dataset.

- **Limitaciones y Consideraciones:**  
  Registrar y documentar las limitaciones del análisis, como la eliminación de filas con missing values, posibles sesgos en la muestra o la necesidad de incorporar ajustes por diseño muestral complejo.

---

## Conclusión

Este documento metodológico abarca desde la descripción y el contenido de los datos obtenidos de los módulos RECH6, RECH0, RECH23 y RECH1, hasta el detalle del procedimiento analítico aplicado, pasando por la configuración de variables y la selección del modelo ordinal. Además, se incluye una guía acerca de la interpretación de los resultados y los diagnósticos realizados, lo cual resulta esencial para validar las afirmaciones del estudio y sentar las bases para futuras mejoras.

Este enfoque permite que otros investigadores o partes interesadas comprendan la metodología del proyecto de forma transparente, facilitando la reproducibilidad y la extensión del análisis en estudios posteriores.

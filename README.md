# Análisis de la Asociación entre el Índice de Bienestar del Hogar y la Anemia en Niños Menores de 5 Años en Perú (ENDES 2023)

## 1. Descripción General

Este proyecto investiga la relación entre el índice de bienestar socioeconómico del hogar y la severidad de la anemia en niños de 6 a 59 meses en Perú, utilizando datos de la Encuesta Demográfica y de Salud Familiar (ENDES) 2023. Se ajusta un modelo de regresión ordinal logit para determinar si los hogares con menor bienestar (medido a través de un índice de riqueza categorizado en quintiles) presentan una mayor probabilidad de tener niños con anemia más grave.

## 2. Hipótesis

| Símbolo              | Formulación                                                                                                                                                                      |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **H₀ (nula)**        | El índice de bienestar del hogar **no** se asocia con la presencia ni la gravedad de la anemia en niños de 6-59 meses.                                                           |
| **H₁ (alternativa)** | El índice de bienestar del hogar **sí** se asocia con la presencia y/o mayor gravedad de la anemia; se espera mayor riesgo de anemia severa en los quintiles de menor bienestar. |

## 3. Estructura del Proyecto

```
endes_anemia/
│
├─ data/                
│   ├─ RECH6_2023.csv         # Datos del niño (edad, sexo, nivel de anemia, etc.)
│   ├─ RECH0_2023.csv         # Datos del hogar (cluster, estrato, ponderadores)
│   ├─ RECH23_2023.csv        # Información de la vivienda e índice de riqueza (HV270, HV271)
│   └─ RECH1_2023.csv         # Datos del roster familiar (edad y educación de la madre)
│
├─ outputs/                 
│   ├─ anemia_clean.parquet   # Dataset limpio y fusionado generado
│   ├─ modelo_ordinal.txt     # Resumen del modelo de regresión ordinal
│   └─ figuras/               # Gráficos y visualizaciones (si los hay)
│
├─ src/                     
│   ├─ 01_read_merge.py       # Script para la lectura, fusión y limpieza de datos
│   └─ 02_model_ordinal.py    # Script para el ajuste del modelo ordinal logit
│
└─ README.md                  # Este documento
```

## 4. Instalación y Requisitos

### Requisitos
- Python 3.10+  
- Paquetes: `pandas`, `numpy`, `statsmodels`, `pyreadstat`, `matplotlib`, `seaborn`

### Instalación
Puedes instalar los paquetes necesarios utilizando pip:

```bash
pip install pandas numpy statsmodels pyreadstat matplotlib seaborn
```

## 5. Metodología

### 5.1. Lectura y Unión de Datos
- **Fuentes de datos:**  
  Se hace uso de cuatro archivos CSV:
  - **RECH6_2023.csv:** Contiene información sobre la anemia, la edad y el sexo de los niños, y un identificador (`HC60`) para enlazar datos de la madre.
  - **RECH0_2023.csv:** Aporta datos del hogar, incluyendo variables de diseño muestral (cluster, estrato y el factor de ponderación `HV005`).
  - **RECH23_2023.csv:** Contiene información sobre la vivienda y el índice de riqueza (`HV270` y `HV271`).
  - **RECH1_2023.csv:** Proporciona datos del roster familiar, en particular, la edad y el nivel educativo de la madre (renombrado como `edu_sup`).

- **Fusión de Datos:**  
  Se unen los archivos utilizando la llave `HHID` (y `HC60` para conectar datos de RECH6 y RECH1) para construir un único dataset.

### 5.2. Limpieza y Transformación de Datos
- **Filtrado:**  
  Se seleccionan únicamente los registros de niños de 6 a 59 meses y se excluyen aquellos con valores no válidos en la variable de anemia.
- **Creación de Variables Derivadas:**  
  - Se define la variable `quintil` a partir de `HV270` (ya categorizado en 1 a 5).
  - Se recodifica el sexo del niño (`HC27`) a una variable binaria (`sexo_nino`).
  - Se calcula la variable `peso` a partir de `HV005` (dividido por 1,000,000).
  - Se crea una variable binaria de anemia (`anemia_bin`) para análisis complementarios.

### 5.3. Modelado Estadístico
- Se ajusta un **modelo de regresión ordinal logit** usando `OrderedModel` de statsmodels.
- Las variables predictoras incluyen:  
  - `quintil` (índice de bienestar),  
  - `HC1` (edad del niño),  
  - `sexo_nino`,  
  - `edad_madre` y  
  - `edu_sup` (nivel educativo de la madre).
- Se incluyen ponderadores derivados de `HV005` para respetar el diseño muestral.

### 5.4. Interpretación de Resultados
- Se examina el summary del modelo, en el que:
  - Los coeficientes y sus odds ratios explican la magnitud del efecto.
  - Los parámetros de corte indican los umbrales del modelo ordinal.

## 6. Resultados Iniciales

- **Dataset Limpio:**  
  Se generó un archivo `anemia_clean.parquet` con 19,265 registros.
  
- **Modelo Ordinal:**  
  El modelo muestra que, por cada incremento en el quintil del índice de bienestar, se incrementan las odds de que el niño se encuentre en una categoría de anemia menos grave (Odds Ratio ≈ 1.26). Asimismo, variables como la edad del niño, el sexo, la edad y la educación de la madre resultaron significativas.

## 7. Próximos Pasos y Mejoras

- **Incluir Variables Adicionales:**  
  Agregar covariables relacionadas a las condiciones ambientales (acceso al agua, saneamiento, combustible) y otras características del hogar.
  
- **Ajuste por Diseño Muestral Complejo:**  
  Explorar métodos que permitan incorporar la estratificación y el clustering en las inferencias (por ejemplo, a través de `statsmodels-survey` o exportando a R).
  
- **Validación del Modelo:**  
  Realizar diagnósticos del modelo mediante análisis de residuales, validación cruzada y exploración de posibles interacciones o efectos no lineales.
  
- **Visualización:**  
  Crear gráficos que ilustren la distribución del índice de bienestar, los efectos predichos y los odds ratios, para facilitar la comunicación de los hallazgos.

## 8. Ejecución

Para reproducir el análisis:
1. Ejecuta el script `src/01_read_merge.py` para generar el dataset limpio (`anemia_clean.parquet`).
2. Ejecuta el script `src/02_model_ordinal.py` para ajustar el modelo ordinal y guardar el resumen en `outputs/modelo_ordinal.txt`.

## 9. Contacto y Referencias

- **Autor:** Universidad Nacional de Cañete
- **Email:** 2101080336@undc.edu.pe
- **Referencias:**  
  - [Documentación de statsmodels OrderedModel](https://www.statsmodels.org/stable/generated/statsmodels.miscmodels.ordinal_model.OrderedModel.html)
  - [ENDES - Instituto Nacional de Estadística e Informática (INEI)](https://www.inei.gob.pe)

```



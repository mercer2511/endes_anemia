### Título Tentativo  
*Relación entre el Índice de Bienestar Socioeconómico del Hogar y la Prevalencia de Anemia en Niños Menores de 5 Años en Perú: Un Análisis de la ENDES 2023*

---

### Planteamiento del Problema  
La anemia en niños menores de 5 años es un problema de salud pública relevante en Perú, asociado a complicaciones en el desarrollo físico y cognitivo y a consecuencias a largo plazo en la productividad y el bienestar. Diversos estudios sugieren que factores socioeconómicos, como el nivel de bienestar del hogar, influyen de manera sustancial en la nutrición y la salud infantil.  
Sin embargo, no se ha profundizado lo suficiente en cómo se relaciona el índice de bienestar—calculado a partir de características de la vivienda y la tenencia de bienes—con la presencia y la gravedad de la anemia durante la infancia.  
El presente estudio busca determinar la existencia de una asociación significativa entre el índice de bienestar del hogar y la clasificación de la anemia infantil, empleando la Encuesta Demográfica y de Salud Familiar (ENDES) 2023.

---

### Variables  

| Tipo                      | Contenido                                                                                                                                                                                                                                                                                                         | Detalle ENDES 2023                                                                                                                                     |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| *Dependiente*             | Anemia en niños de 6-59 meses                                                                                                                                                                                                                                                                                     | Variable HC57 (o HW57) <br>1 = grave, 2 = moderada, 3 = leve, 4 = sin anemia <br>También se puede recodificar a binaria (anémico = 1, no anémico = 0). |
| *Independiente principal* | Índice de Bienestar (nivel socioeconómico)                                                                                                                                                                                                                                                                        | Puntaje o quintil HV270 del módulo *RECH0*.                                                                                                            |
| *Covariables clave*       | • Edad del niño (meses) HC <br>• Sexo del niño (del roster HV104) <br>• Edad de la madre HV105 <br>• Nivel educativo materno HV106/HV109 <br>• Área de residencia HV025, región HV024 <br>• Fuente de agua HV201, saneamiento HV205, combustible HV226 (RECH23) <br>• Seguro de salud materno SH11C (SIS) (RECH4) |

---

### Hipótesis  

| Símbolo            | Formulación                                                                                                                                                                    |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *H₀ (nula)*        | El índice de bienestar del hogar *no* se asocia con la presencia ni la gravedad de la anemia en niños de 6-59 meses.                                                           |
| *H₁ (alternativa)* | El índice de bienestar del hogar *sí* se asocia con la presencia y/o mayor gravedad de la anemia; se espera mayor riesgo de anemia severa en los quintiles de menor bienestar. |

---

### Método Estadístico Sugerido  

1. *Regresión ordinal (modelo logit acumulativo / proporcional de odds)*  
   - Variable respuesta: nivel de anemia (4 categorías ordenadas).  
   - Predictora principal: quintil de riqueza.  
2. *Diseño muestral complejo*  
   - Cluster: HV001  
   - Estrato: HV022  
   - Peso: HV005 / 1 000 000  
   - En Python se puede ajustar con statsmodels.miscmodels.ordinal_model.OrdinalModel y errores robustos ponderados; para varianzas tipo‐Taylor, considerar el paquete **statsmodels-survey** o exportar a R (survey/srvyr).  
3. *Análisis complementarios*  
   - Regresión logística binaria (anémico vs. no anémico) para comparar con la ordinal.  
   - Modelos de sensibilidad con distintos subconjuntos (área urbana/rural, altitud > 2500 m, etc.).  
   - Descriptivos y mapas de calor para visualizar la distribución de anemia por quintil y región.

---

### Recomendaciones para Usar la Base ENDES  

1. *Módulos CSV mínimos* 

   | Propósito                                 | Archivo CSV         | Identificadores clave                   |
   |-------------------------------------------|---------------------|-----------------------------------------|
   | Anemia y edad del niño                    | *RECH6* (HHID, HC0) | HHID, HC0, HC57, HC                     |
   | Bienestar y ponderadores                  | *RECH0*             | HHID, HV270, HV001, HV022, HV005        |
   | Datos de la madre                         | *RECH1*             | HHID, HVIDX, HV105, HV106, HV109, HV112 |
   | Seguro/ocupación de la madre (opcional)   | *RECH4*             | HHID, IDXH4, SH11C                      |
   | Agua, saneamiento, combustible (opcional) | *RECH23*            | HHID, HV201, HV205, HV226, HV237*       |

2. *Enlace de módulos*  
   - HHID enlaza hogar ↔ niño/madre.  
   - Línea de madre: HV112 (en RECH1) = HC60 (en RECH6).  

3. *Depuración y validación*  
   - Filtrar niños de 6–59 meses (HC between 6 and 59).  
   - Excluir códigos faltantes (9996/9997/9998).  
   - Recalcular quintiles si prefieres usar la distribución ponderada 2023.  

4. *Aplicación de pesos y estratos*  
   - Declarar diseño muestral en el software elegido para obtener *intervalos de confianza y p-valores correctos*.  

---

### Tipo de Investigación  

| Aspecto         | Descripción                                                                                    |
|-----------------|------------------------------------------------------------------------------------------------|
| Diseño          | Observacional transversal (análisis secundario de la ENDES 2023).                              |
| Enfoque         | Cuantitativo analítico.                                                                        |
| Fuente de datos | Encuesta Demográfica y de Salud Familiar (ENDES) – muestra compleja estratificada & ponderada. |

---

## Recapitulación final  
CSV que realmente necesitas descargar/cargar para un *primer modelo ordinal* (bienestar → anemia) y los que puedes añadir después como extras.

| Prioridad | Archivo CSV | Variables que extraer                   | Para qué se usa                                                                                            |
|-----------|-------------|-----------------------------------------|------------------------------------------------------------------------------------------------------------|
| ★ Básico  | *RECH6*     | HHID, HC0, HC60, HC, HC27, HC57         | Genera la tabla de niños 6-59 m (con edad, sexo y NIVEL DE ANEMIA).                                        |
| ★ Básico  | *RECH0*     | HHID, HV001, HV022, HV005               | Ponderador del hogar (HV005/1e6) + cluster (HV001) + estrato (HV022).                                      |
| ★ Básico  | *RECH23*    | HHID, HV270 (ó HV270, HV271)            | Índice/quintil de riqueza (si *RECH0* ya lo trae, RECH23 se vuelve opcional).                              |
| ★ Básico  | *RECH1*     | HHID, HVIDX, HV104, HV105, HV106, HV109 | Características de la madre (edad, educación) y del niño (sexo). <br>Enlazas con línea-madre HV112 = HC60. |

### Total imprescindible: *3 CSV*  
(4 CSV si HV270 no está en tu RECH0 y lo lees desde RECH23).

---

### Extras útiles para modelos más completos

| Archivo  | Variables                   | Aporte                                                                    |
|----------|-----------------------------|---------------------------------------------------------------------------|
| *RECH4*  | HHID, IDXH4, SH11C          | Cobertura SIS, actividad laboral materna (SH13).                          |
| *RECH23* | HV201, HV205, HV226, HV237* | Agua, saneamiento, combustible, tratamiento del agua (control ambiental). |
| *RECHM*  | HHID, NRO_ORDEN_ID y causa  | Bandera de “madre fallecida” o mortalidad reciente.                       |

Empieza con los *básicos* para un flujo amigable; añade los “extras” cuando tu equipo quiera profundizar en confusores.

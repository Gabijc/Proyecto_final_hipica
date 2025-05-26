# Una mirada analítica al deporte ecuestre

![Salto de obstáculos](Documentation/foto_readme.JPG)

## 📖 Descripción

La hípica es uno de los deportes más complejos a día de hoy. Se ve influido por múltiples factores más allá del rendimiento individual del jinete o del caballo, haciendo que el análisis de resultados de las competiciones sea especialmente desafiante. Además, la escasa disponibilidad de datos dificulta tanto la toma de decisiones como la comprensión del deporte por parte de su audiencia.

Este proyecto nace para dar valor a la competición ecuestre a través del análisis de datos, con el objetivo de mejorar la comprensión, la toma de decisiones y la comunicación en el entorno de la hípica. Para ello se ha desarrollado un dashboard interactivo que presenta insights clave sobre las competiciones, un entorno de acceso a datos de concursos y binomios (jinete y caballo), así como un sistema de análisis del rendimiento de los binomios. Con esta iniciativa, se busca transformar los datos en una herramienta estratégica, impulsando el desarrollo y la visibilidad del deporte ecuestre.

## 🗂️ Estructura del Proyecto

```  
/Proyecto_final_hipica
│
├── /data/                                      # Carpeta para almacenar los datos crudos y procesados.
|        ├── data_completo                      # Datos de concurso completo.
|        ├── data_salto                         # Datos de salto de obstáculos.
|
├── /Documentation/                             # Notebooks de Jupyter con con análisis preliminares, pruebas de código y exploración de datos.
|        ├── /Entregables/                      # Directorio que contiene los entregables realizados durante el proyecto.
|        ├── /Reglamentos/                      # Directorio que contiene el reglamento de las disciplinas de salto de obstáculos y concurso completo.
|        ├── Memoria_proyecto_final.pdf         # Informe detallado del proceso seguido en el proyecto.
|        ├── ERD_BBDD_Hipica.png                # Esquema entidad relación de la base de datos.
|        └── Script_Creacion_BBDD.sql           # Script de creación de la base de datos.
|
├── /Notebooks/                                 # Notebooks de Jupyter con con análisis preliminares, pruebas de código y exploración de datos.
|        ├── scrapeo_concursos_salto.ipynb      # Proceso de extracción de los datos de la disciplina de salto de obstáculos.
|        ├── scrapeo_concursos_completo.ipynb   # Proceso de extracción de los datos de la disciplina de concurso completo.
|        ├── union_datos_scrapeados.ipynb       # Limpieza y unión en un mismo dataset de los resultados obtenidos.
|        ├── EDA.ipynb                          # Análisis exploratorio de los datos obtenidos, y creación de visualizaciones e insights relevantes.
|        └── carga_BBDD.ipynb                   # Carga de los datos extraídos a la base. 
|        
├── /src/                                       # Scripts de procesamiento y modelado
|        ├── soporte_extraccion_salto.py        # Funciones auxiliares para la extracción y limpieza de los datos extraídos de la disciplina de salto de obstáculos.
|        ├── soporte_extraccion_completo.py     # Funciones auxiliares para la extracción y limpieza de los datos extraídos de la disciplina de concurso completo.
|        ├── soporte_extraccion_general.py      # Funciones auxiliares para la extraccion de datos de forma general para las disciplinas analizadas.
|        └── soporte_carga_dashboard.py         # Funciones auxiliares para realizar la carga a la base de datos y generar visualizaciones e insights.
|
├── extraccion_salto.py                         # Script para realizar el proceso de ETL de la disciplina de salto de obstáculos.
├── extraccion_completo.py                      # Script para realizar el proceso de extracción de la disciplina de concurso completo.
├── app.py                                      # Script de creación del dashboard interactivo, y acceso a los resultados de concursos. 
├── README.md                                   # Descripción del proyecto
├── requirements.txt                            # Archivo de dependencias para el proyecto
```
  
## 🛠️ Instalación y Requisitos
    
Este proyecto usa Python 3.12.4. Para configurarlo, sigue los siguientes pasos.

1. Clona el repositorio: `` git clone  https://github.com/Gabijc/Proyecto_final_hipica.git ``
2. Instala las dependencias necesarias: ``pip install -r requirements.txt ``
3. Ejecuta los archivos .py para la extracción, transformación y carga de los datos: `` python nombre_archivo.py ``
5. Lanza en dashboard de streamlit: ``streamlit run app.py``

Las librerías requeridas son:

- **pandas**: manejo y análisis de datos estructurados.
- **numpy**: cálculos numéricos y operaciones con arrays.
- **plotly express**: visualización avanzada.
- **psycopg2**: conexión y manipulación a bases de datos PostgreSQL en Python.
- **selenium**: realización de web scraping.
- **webdriver_manager**: gestión del WebDriver para selenium.
- **streamlit**: desarrollo dashboards interactivos para visualización de datos y resultados del análisis.
- **Dbeaver (opcional)**: gestión de bases de datos.


## 📊 Resultados y Conclusiones

En este proyecto vemos una representación de técnicas de análisis de datos en la competición hípica en España. Se ha generado un proceso de recolección de información que facilita la actualización continua de datos, suponiendo esto una base sólida para futuros análisis. 

A través de la herramienta creada haciendo uso de streamlit, se puede realizar un análisis del rendimiento de los binomios, hacer un overview de las competiciones hípicas en España, además de ser una forma de acceso sencilla y al alcance de todos de información sobre los concursos de salto de obstáculos en España.

Observamos los siguientes resultados:

- Se han celebrado un total de 122 concursos, entre el 2025-01-10 y el 2025-04-27, siendo una gran parte de ámbito internacional. El mes que más concursos se han realizado ha sido febrero, con un total de 41 concursos, y el mes que menos concursos se han realizado ha sido el mes de abril, con un total de 21 concursos. 
- Un 61,48 \% de los concursos se han realizado en la provincia de Valencia.
- De media, en un concurso se realizan 13 pruebas, y los tipo de prueba más aplicados son: Baremo A con cronómetro (238.2.1); Baremo A con cronómetro y desempate (238.2.2);Dos fases, ambas con cronómetro (274.1.5.3); Dos fases especial (274.2).
- Se han realizado concursos de competiciones de entre una y cinco estrellas, además de concursos de caballos jóvenes (YH), y de las categorías de children, y jóvenes jinetes (Ch/J/Y). 
- Han participado un total de 9.012 binomios, y se ha analizado que, de media, un jinete sale a pista con tres caballos diferentes. Del total de caballos que tenemos, que son 8.333, un 21,44 \% se consideran caballos jóvenes, ya que han participado en pruebas de 5, 6 y 7 años. 

## 🔄 Próximos Pasos

Se plantean a continuación una serie de líneas de trabajo para desarrollar a futuro:

- Generar un análisis histórico y detallado de la competición de las disicplinas olímpicas, tanto a nivel nacional, como a nivel internacional. 
- Información sobre ingresos/costes a través de los avances de programa de cada competición hípica, así como de los Fei Annual Reports, de manera que se pueda realizar un análisis de ingresos/costes de las competiciones.
- Crear un sistema predictivo que permita hacer pronósticos sobre los resultados en futuras competiciones.
- Realizar la corrección de errores menores en la base de datos.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un pull request o una issue.

## ✒️ Autores
**Gabriela Jiménez Conde** - [gabrielajimenezconde@gmail.com](https://github.com/Gabijc)
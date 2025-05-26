# Una mirada analítica al deporte ecuestre

## 📖 Descripción


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
|        ├── Informe_final.pdf                  # Informe detallado del proceso seguido en el proyecto.
|        ├── ERD_BBDD_Hipica.png                # Esquema entidad relación de la base de datos.
|        └── Script_Creacion_BBDD.sql           # Script de creación de la base de datos.
|
├── /Notebooks/                                 # Notebooks de Jupyter con con análisis preliminares, pruebas de código y exploración de datos.
|        ├── scrapeo_concursos_salto.ipynb             # Análisis y limpieza de los datos obtenidos.
|        ├── scrapeo_concursos_completo.ipynb                 # Web scraping de los hoteles de la competencia.
|        ├── union_datos_scrapeados.ipynb               # Extracción de información de eventos de una API.
|        ├── EDA.ipynb           # Conexión y carga de los datos a la base de datos.
|        └── carga_BBDD.ipynb                  # Análisis de la información de la base de datos. 
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
├── requirements.txt                           # Archivo de dependencias para el proyecto
```
  
## 🛠️ Instalación y Requisitos
    
Este proyecto usa Python 3.12.4. Para configurarlo, sigue los siguientes pasos.

1. Clona el repositorio:

`` git clone  https://github.com/Gabijc/Proyecto_final_hipica.git ``

2. Instala las dependencias necesarias:

``pip install -r requirements.txt ``

3. Ejecuta los archivos .py para la extracción, transformación y carga de los datos.
5. Lanza en dashboard de streamlit:

``streamlit run app.py``

Las librerías requeridas son:

- **pandas**: manejo y análisis de datos estructurados.
- **numpy**: cálculos numéricos y operaciones con arrays.
- **plotly express**: visualización avanzada.
- **psycopg2**: conexión y manipulación a bases de datos PostgreSQL en Python.
- **selenium**: realización de web scraping.
- **webdriver_manager**: gestión del WebDriver para selenium.
- **Streamlit**: 
- **Dbeaver (opcional)**: gestión de bases de datos.


## 📊 Resultados y Conclusiones



## 🔄 Próximos Pasos


## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un pull request o una issue.

## ✒️ Autores
**Gabriela Jiménez Conde** - [gabrielajimenezconde@gmail.com](https://github.com/Gabijc)
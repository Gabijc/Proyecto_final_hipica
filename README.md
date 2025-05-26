# Una mirada analítica al deporte ecuestre

## 📖 Descripción


## 🗂️ Estructura del Proyecto

```  
/Proyecto_final_hipica
│
├── /data/                                      # Carpeta para almacenar los datos crudos y procesados.
|        ├── hoteles_competencia.csv            # Datos de eventos de Madrid obtenidos desde una API.
|        ├── hoteles_competencia.csv            # Datos de hoteles de la competencia obtenidos por scraping.
|        ├── reservas_hoteles_limpio.csv        # Datos de hoteles del grupo y de la competencia limpios.
|        └── reservas_hoteles.parquet           # Datos de hoteles del grupo.
|
├── /notebooks/                                  # Notebooks de Jupyter con con análisis preliminares, pruebas de código y exploración de datos.
|        ├── Análisis_inicial.ipynb             # Análisis y limpieza de los datos obtenidos.
|        ├── Scrapeo_info.ipynb                 # Web scraping de los hoteles de la competencia.
|        ├── Extraccion_api.ipynb               # Extracción de información de eventos de una API.
|        ├── Carga_BBDD_Hoteles.ipynb           # Conexión y carga de los datos a la base de datos.
|        ├── Bonus_track.ipynb                  # Análisis de la información de la base de datos.
|        └──  Script_Creacion_BBDD_Hoteles.sql  # Script de creación de la base de datos.
|        
├── /src/                                       # Scripts de procesamiento y modelado
|        ├── soporte_carga.py                   # Funciones auxiliares para la carga de datos a la base.
|        ├── soporte_limpieza.py                # Funciones auxiliares para la limpieza y el procesamiento de datos.
|        ├── soporte_extraccion.py              # Funciones auxiliares para la extraccion de datos mediante web scraping y APIs.
|        └── soporte_informe.py                 # Funciones auxiliares para generar visualizaciones e insights.
|
├── main_carga.py                               # Script para realizar la carga de datos a la base.
├── main_extraccion.py                          # Script para realizar el scraping de datos de la competencia y las llamadas a la API. 
├── main_informe.py                             # Script para realizar el scraping de datos de la competencia
├── main_limpieza.py                            # Script para realizar la limpieza de los datos.
├── main.py                                     # Script para realizar el proceso de ETL y la generación de insights.
├── app.py                                      # Script de creación de un dashbaord interactivo
├── README.md                                   # Descripción del proyecto
├── /requirements.txt                           # Archivo de dependencias para el proyecto
├── .env                                        # Archivo de variables de entorno (no debe subirse al repositorio)
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
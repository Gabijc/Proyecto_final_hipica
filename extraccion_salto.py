from src.soporte_extraccion_salto import extraccion_salto_nac, extraccion_salto_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_salto")
ruta_pruebas = os.getenv("ruta_pruebas_salto")
ruta_enlaces_resultados = os.getenv("ruta_urls_salto")

rutas = [ruta_concursos, ruta_pruebas, ruta_enlaces_resultados]
url = url_scrapeo

if __name__ == "__main__":

    condicion = 1

    if condicion == 1:
        extraccion_salto_nac(url, lista_rutas = rutas)
        extraccion_salto_int(url)

    else: 
        print("coso")
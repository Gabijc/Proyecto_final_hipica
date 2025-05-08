from src.soporte_extraccion_doma import extraccion_doma_nac, extraccion_doma_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_doma")
ruta_pruebas = os.getenv("ruta_pruebas_doma")
ruta_enlaces_resultados = os.getenv("ruta_urls_doma")

rutas = [ruta_concursos, ruta_pruebas, ruta_enlaces_resultados]
url = url_scrapeo

if __name__ == "__main__":
    condicion = 1
    if condicion == 1: 
        extraccion_doma_nac(url)
        extraccion_doma_int(url)
    else:
        print("coso")
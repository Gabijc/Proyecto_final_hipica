from src.soporte_extraccion_completo import extraccion_completo_nac, extraccion_completo_int
import os 
from dotenv import load_dotenv


load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_completo")
ruta_pruebas = os.getenv("ruta_pruebas_completo")
ruta_enlaces_resultados = os.getenv("ruta_urls_completo")

rutas = [ruta_concursos, ruta_pruebas, ruta_enlaces_resultados]
url = url_scrapeo

if __name__ == "__main__":

    extraccion_completo_nac(url)
    extraccion_completo_int(url)
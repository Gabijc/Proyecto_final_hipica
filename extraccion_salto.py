from src.soporte_extraccion_salto import extraccion_salto_nac, extraccion_salto_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_completo")

rutas = [ruta_concursos, ruta_pruebas, ruta_enlaces]
url = url_scrapeo

if __name__ == "__main__":
 
    extraccion_salto_nac(url, lista_rutas = )
    extraccion_salto_int(url)
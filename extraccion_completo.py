from src.soporte_extraccion_completo import extraccion_completo_nac, extraccion_completo_int, extraccion_resultados_jinetes_caballos
from src.soporte_extraccion_general import get_competiciones, descarga_excels
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_completo")
ruta_pruebas = os.getenv("ruta_pruebas_completo")
ruta_enlaces_resultados = os.getenv("ruta_urls_completo")
lista_urls = ""
rutas = [ruta_concursos, ruta_pruebas, ruta_enlaces_resultados]
url = url_scrapeo

if __name__ == "__main__":

    condicion = 2

    if condicion == 1:

        extraccion_completo_nac(url, lista_rutas = rutas)
        extraccion_completo_int(url, lista_rutas = rutas)

    elif condicion == 2:
        # me hace la extracicon de los excels
        driver = get_competiciones("https://gestion.cbservicios.net/RFHE_RESULTADOS_WEB/ES/PAGE_CCM_Resultados_2.awp?P1=227038&AWPIDA8F4E70E=21CF0AFEB537B76BC223AA2FF731C07F6FD1A148")
        descarga_excels(driver)

    elif condicion == 3:
        # me hace la extraccion de jinetes
        extraccion_resultados_jinetes_caballos(lista_urls)
    else: 
        # me lanza todo
        extraccion_completo_nac(url)
        extraccion_completo_int(url)
        extraccion_resultados_jinetes_caballos(lista_urls)
        
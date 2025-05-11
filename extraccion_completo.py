from src.soporte_extraccion_completo import extraccion_completo_nac, extraccion_completo_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_completo")
ruta_pruebas = os.getenv("ruta_pruebas_completo")
ruta_resultados = os.getenv("ruta_resultados_completo")
lista_urls = ""
rutas = [ruta_concursos, ruta_pruebas, ruta_resultados]
url = url_scrapeo

if __name__ == "__main__":

    condicion = 1

    if condicion == 1:

        extraccion_completo_nac(url, lista_rutas = rutas)
        extraccion_completo_int(url, lista_rutas = rutas)

    elif condicion == 2:
        # me hace la extracicon de los excels
        print("Ok")
        #descarga_excels(ruta_carpeta_guardado = ruta_resultados_buenos, ruta_carpeta_lectura = ruta_enlaces_resultados, disciplina = "completo")

    elif condicion == 3:
        # me hace la extraccion de jinetes
        #extraccion_resultados_jinetes_caballos(lista_urls)
        print("no")
    else: 
        # me lanza todo
        extraccion_completo_nac(url)
        extraccion_completo_int(url)
        #extraccion_resultados_jinetes_caballos(lista_urls)
        print("ok")
        
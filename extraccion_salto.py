from src.soporte_extraccion_salto import extraccion_salto_nac, extraccion_salto_int
from src.soporte_extraccion_general import descargar_excel, lectura_excels
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_salto")
ruta_pruebas = os.getenv("ruta_pruebas_salto")
ruta_resultados = os.getenv("ruta_resultados_salto")
lista_urls = ""

rutas = [ruta_concursos, ruta_pruebas]
url = url_scrapeo

if __name__ == "__main__":

    condicion = 1

    if condicion == 1:

        urls_nacionales = extraccion_salto_nac(url, lista_rutas = rutas)
        descargar_excel(lista_urls = urls_nacionales, ruta_guardado = ruta_resultados, disciplina = "salto")
        

    elif condicion == 2:
        
        urls_int = extraccion_salto_int(url, lista_rutas = rutas)
        descargar_excel(lista_urls = urls_int, ruta_guardado = ruta_resultados, disciplina = "salto")

    elif condicion == 3:
        lectura_excels(ruta_resultados)
    
    else:
        print("mal")

    # elif condicion == 3:
    #     # me hace la extraccion de jinetes
    #     extraccion_resultados_jinetes_caballos(lista_urls)
        
    # else: 
    #     # me lanza todo
    #     extraccion_salto_nac(url, lista_rutas = rutas)
    #     extraccion_salto_int(url)
    #     extraccion_resultados_jinetes_caballos(lista_urls)
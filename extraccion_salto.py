from src.soporte_extraccion_salto import extraccion_salto_nac, extraccion_salto_int, mergeo_dfs
from src.soporte_extraccion_general import descargar_excel, limpieza_excels 
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")
ruta_concursos = os.getenv("ruta_concursos_salto")
ruta_pruebas = os.getenv("ruta_pruebas_salto")
ruta_resultados = os.getenv("ruta_resultados_salto")
ruta_resultados_lectura_25 = os.getenv("ruta_lectura_json_resultados_25")
ruta_resultados_25 = os.getenv("ruta_resultados_25")
lista_urls = ""
rutas = [ruta_concursos, ruta_pruebas, ruta_resultados]
url = url_scrapeo
ruta_guardado_excels_combinados = os.getenv("ruta_guardado_excels_combinados")
ruta_df_concursos = os.getenv("ruta_df_concursos")
ruta_df_pruebas = os.getenv("ruta_df_pruebas")
ruta_guardado_df_final = os.getenv("ruta_guardado_df_final")



if __name__ == "__main__":

    condicion = 2

    if condicion == 1:

        extraccion_salto_nac(url, lista_rutas = rutas)
        extraccion_salto_int(url, lista_rutas = rutas)
        
        
    elif condicion == 2:
        descargar_excel(ruta_lectura=ruta_resultados_lectura_25, ruta_guardado = ruta_resultados_25, disciplina = "salto")

    elif condicion == 3:
        limpieza_excels(ruta_resultados, ruta_guardado_excels_combinados)
        mergeo_dfs(ruta_df_concursos = ruta_df_concursos, ruta_df_pruebas = ruta_df_pruebas, ruta_guardado_df_final = ruta_guardado_df_final)
        
    else: 
        # me lanza todo
        extraccion_salto_nac(url, lista_rutas = rutas)
        extraccion_salto_int(url)
        descargar_excel(ruta_lectura=ruta_resultados_lectura_25, ruta_guardado = ruta_resultados_25, disciplina = "salto")
        limpieza_excels(ruta_resultados, ruta_guardado_excels_combinados)
        mergeo_dfs(ruta_df_concursos = ruta_df_concursos, ruta_df_pruebas = ruta_df_pruebas, ruta_guardado_df_final = ruta_guardado_df_final)
         
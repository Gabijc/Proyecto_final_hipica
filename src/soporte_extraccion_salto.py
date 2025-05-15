# Importamos las librerías necesarias
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
import re
import pandas as pd
from src.soporte_extraccion_general import get_competiciones, cambio_pestaña, resultados_disciplina, buscador_elementos, guardado_info, competiciones_año, obtencion_año, creacion_dictios_guardado, extraccion_info_concursos, extraccion_info_pruebas
from src.soporte_extraccion_general import archivos

def extraccion_salto_nac(url, lista_rutas): 

    dictio_concursos_salto_nac, dictio_pruebas_salto_nac = creacion_dictios_guardado()
    urls_resultados_salto_nac = []

    driver = get_competiciones(url, lista_rutas[0])
    time.sleep(2)

    # Seleccionamos el ambito de los concursos y la disciplina, en este caso nacional y completo
    ambito_buscado, disciplina_buscada = resultados_disciplina(driver, disciplina = "salto")
    cambio_pestaña(1,driver)
    time.sleep(2)
 
    año = obtencion_año(driver)

    while año >= 2017:

        # vamos a todos los concursos del año en el que estemos
        competiciones_año(driver)

        maximo_n_concursos = int(buscador_elementos(driver, "/html/body/form/div/div/div/ul/li[13]/font").text.split(" ")[-1].replace("(", "").replace(")", ""))
        if año == 2025:
            rango = range(5,139)
        elif año < 2025:
            rango = range(5, maximo_n_concursos + 5) 

        for i in rango:

            try:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/a")
                print(concurso_bueno.text)
                time.sleep(1)
                try:
                    concurso_bueno.click()
                    cambio_pestaña(2, driver)
                    time.sleep(2)
                    contenido_general =  buscador_elementos(driver, "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table").text.split('\n')
                                                                    
                    if "Resultados: Ver resultados  Ver" not in contenido_general:
                        driver.close()
                        cambio_pestaña(1, driver)
                        time.sleep(1)
                    
                    elif "Resultados: Ver resultados  Ver" in contenido_general:
                        print(contenido_general)
                        
                        extraccion_info_concursos(driver, diccionario_concursos=dictio_concursos_salto_nac, ambito_buscado=ambito_buscado, contenido_general=contenido_general)
                        time.sleep(2)
                        
                        try:
                            cambio_pestaña(3, driver)
                            time.sleep(2)
                            extraccion_info_pruebas(driver, dictio_concursos_salto_nac, dictio_pruebas_salto_nac, urls_resultados_salto_nac)

                            driver.close()
                            cambio_pestaña(2, driver)
                            driver.close()
                            cambio_pestaña(1, driver)
                            time.sleep(2)

                        except IndexError:
                            time.sleep(10)
                            driver.refresh()
                            try:
                                extraccion_info_concursos(driver, dictio_concursos_salto_nac, dictio_pruebas_salto_nac, urls_resultados_salto_nac)
                                driver.close()
                                cambio_pestaña(1, driver)
                            except Exception as e:
                                driver.close()
                                cambio_pestaña(1, driver)
                                print(f"Error ocurrido:{e}")

                except NoSuchElementException:
                    raise NoSuchElementException

            except NoSuchElementException:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/font").text
                print(concurso_bueno)

        lista_archivos = [dictio_concursos_salto_nac, dictio_pruebas_salto_nac, urls_resultados_salto_nac]
        nombres_archivos = archivos(disciplina_buscada, ambito_buscado, año)

        i = 0
        for ruta in lista_rutas:
                 
            with open(f"{ruta}{nombres_archivos[i]}.json", "w", encoding="utf-8") as f:
                        json.dump(lista_archivos[i], f, ensure_ascii=False, indent=4) # se deja la ruta desde la que estoy ejecutando .py, no desde el src
            i += 1
        
        buscador_elementos(driver,"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/a").click()        
        año = obtencion_año(driver)

    driver.quit()


def extraccion_salto_int(url, lista_rutas):
    
    dictio_concursos_salto_int, dictio_pruebas_salto_int = creacion_dictios_guardado()
    urls_resultados_salto_int = []

    # inicializamos el driver y lo abrimos
    driver = get_competiciones(url, lista_rutas[0])
    time.sleep(2)

    # Seleccionamos el ambito de los concursos y la disciplina, en este caso nacional y completo
    ambito_buscado, disciplina_buscada = resultados_disciplina(driver, ambito = "internacional", disciplina = "salto")
    cambio_pestaña(1,driver)
    time.sleep(2)

    año = obtencion_año(driver)

    while año >= 2017:

        # Buscamos los concursos del año que nos aparece
        competiciones_año(driver)

        time.sleep(0.5)

        maximo_n_concursos = int(buscador_elementos(driver, "/html/body/form/div/div/div/ul/li[13]/font").text.split(" ")[-1].replace("(", "").replace(")", ""))
        if año == 2025:
            rango = range(5,154)
        elif año < 2025:
            rango = range(5, maximo_n_concursos + 5) 

        for i in rango:
            
            try:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/a")
                print(concurso_bueno.text)
                time.sleep(1)
                try:
                    concurso_bueno.click()
                    cambio_pestaña(2, driver)
                    time.sleep(2)
                    contenido_general = buscador_elementos(driver, "/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table").text.split('\n')
                                                                    
                    if "Resultados: Ver resultados  Ver" not in contenido_general:
                        driver.close()
                        cambio_pestaña(1, driver)
                        time.sleep(1) 
                    
                    elif "Resultados: Ver resultados  Ver" in contenido_general:
                        print(contenido_general)

                        extraccion_info_concursos(driver, diccionario_concursos=dictio_concursos_salto_int, ambito_buscado=ambito_buscado, contenido_general=contenido_general)
                        time.sleep(2)
                        try:
                            cambio_pestaña(3,driver)
                            time.sleep(2)
                            extraccion_info_pruebas(driver, dictio_concursos_salto_int, dictio_pruebas_salto_int, urls_resultados_salto_int)
                        
                            driver.close()
                            cambio_pestaña(2, driver)
                            driver.close()
                            cambio_pestaña(1, driver)
                            time.sleep(2)
                        except IndexError:
                            time.sleep(5)
                            driver.refresh()
                            try:
                                extraccion_info_concursos(driver, dictio_concursos_salto_int, dictio_pruebas_salto_int, urls_resultados_salto_int)
                                driver.close()
                                cambio_pestaña(1, driver)
                            except Exception as e:
                                driver.close()
                                cambio_pestaña(1, driver)
                                print(f"Error ocurrido:{e}")
                                 

                except NoSuchElementException:
                    raise NoSuchElementException

            except NoSuchElementException:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/font").text
                print(concurso_bueno)
        
        lista_archivos = [dictio_concursos_salto_int, dictio_pruebas_salto_int, urls_resultados_salto_int]
        nombres_archivos = archivos(disciplina_buscada, ambito_buscado, año)

        i = 0
        for ruta in lista_rutas:
                 
            with open(f"{ruta}{nombres_archivos[i]}.json", "w", encoding="utf-8") as f:
                        json.dump(lista_archivos[i], f, ensure_ascii=False, indent=4) # se deja la ruta desde la que estoy ejecutando .py, no desde el src
            i += 1

        buscador_elementos(driver,"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/a").click()
        time.sleep(3)        
        año = obtencion_año(driver)

    driver.quit()
    
def creacion_columnas(df, columna_crear, columna, coso = "paises"):
    posiciones = ["RET", "ELI", "NOP"]

    df[columna] = df[columna].astype(str)
    
    if coso == "paises":
        df[columna_crear] = df[columna].apply(lambda x: x.split("(")[1].strip(")") if x.endswith(")") else "ESP")
        df[columna] = df[columna].apply(lambda x: x.split("(")[0].strip() if x.endswith(")") else x)
    elif coso == "Estado": 
        if "Puntuacion" in df.columns:  
            df["Posicion"] = df.apply(lambda x: "NOP" if pd.isna(x["Puntuacion"]) else x["Posicion"], axis=1)
        df[columna_crear] = df[columna].apply(lambda x: x if x in posiciones else "FIN")
    elif coso == "Premio":
        df[columna_crear] = df[columna].apply(lambda x: False if x == 0 else True)
        
def modificaciones_generales(dataframe):

    dataframe["Prueba"] = dataframe.iloc[3,1]
    dataframe["Categoria"] = dataframe.iloc[4,1]
    dataframe["Fecha_prueba"] = dataframe.iloc[2,1]
    dataframe["Concurso"] = dataframe.iloc[1,1].split("(")[0].strip()
    dataframe = dataframe.iloc[9:].reset_index(drop = True)
    dataframe = dataframe.rename(columns = {"Unnamed: 0": "Posicion", 
                                                 "Unnamed: 1": "Lic_jinete",
                                                 "Unnamed: 2": "Jinete", 
                                                 "Unnamed: 3": "Lic_caballo", 
                                                 "Unnamed: 4": "Caballo",
                                                 "Unnamed: 5": "Raza_caballo",
                                                 "Unnamed: 6": "Puntuacion",
                                                 "Unnamed: 7": "Dinero_premio"})
    dataframe["Raza_caballo"] = dataframe["Raza_caballo"].apply(lambda x: None if x == "--" else x)
    creacion_columnas(dataframe, "Pais_jinete", "Jinete")
    creacion_columnas(dataframe, "Pais_caballo", "Caballo")
    creacion_columnas(dataframe, "Estado", "Posicion", coso = "Estado")
    creacion_columnas(dataframe, "Premio", "Dinero_premio", coso = "Premio")
    dataframe = dataframe.reindex(columns = ['Estado','Posicion', 'Lic_jinete', 'Jinete', 'Pais_jinete', 'Lic_caballo', 'Caballo',
              'Raza_caballo', 'Pais_caballo', 'Puntuacion', 'Premio','Dinero_premio', 'Prueba', 'Fecha_prueba',
              'Concurso', "Categoria"])

    return dataframe

def parse_puntuacion_tupla(puntuacion_str):
    """
    Parsea la cadena de puntuación y devuelve una tupla con los valores
    para las nuevas columnas.
    """
    resultados = str(puntuacion_str).split('\n')
    ptos_obs = [None] * 3
    ptos_tiempo = [None] * 3
    tiempo = [None] * 3

    # Caso específico 1: numero\nnumero(Obs - Tpo)/tiempo
    match_caso1 = re.match(r'(\d+)\n(\d+)\((\d+) Obs - (\d+) Tpo\)/([\d,]+)', puntuacion_str)
    if match_caso1:
        ptos_obs[0] = int(match_caso1.group(1))
        ptos_obs[1] = int(match_caso1.group(3))
        ptos_tiempo[1] = int(match_caso1.group(4))
        tiempo[1] = float(match_caso1.group(5).replace(',', '.'))
        return (ptos_obs[0], ptos_tiempo[0], tiempo[0],
                ptos_obs[1], ptos_tiempo[1], tiempo[1],
                ptos_obs[2], ptos_tiempo[2], tiempo[2])

    # Caso específico 2: numero(Obs - Tpo)\nnumero(Obs - Tpo)/tiempo
    match_caso2 = re.match(r'(\d+)\((\d+) Obs - (\d+) Tpo\)\n(\d+)\((\d+) Obs - (\d+) Tpo\)/([\d,]+)', puntuacion_str)
    if match_caso2:
        ptos_obs[0] = int(match_caso2.group(2))
        ptos_tiempo[0] = int(match_caso2.group(3))
        ptos_obs[1] = int(match_caso2.group(5))
        ptos_tiempo[1] = int(match_caso2.group(6))
        tiempo[1] = float(match_caso2.group(7).replace(',', '.'))
        return (ptos_obs[0], ptos_tiempo[0], tiempo[0],
                ptos_obs[1], ptos_tiempo[1], tiempo[1],
                ptos_obs[2], ptos_tiempo[2], tiempo[2])

    # Procesamiento por línea si no coinciden los casos específicos
    for i, resultado in enumerate(resultados[:3]):
        obs_tiempo_barra_match = re.match(r'(\d+)\((\d+) Obs - (\d+) Tpo\)/([\d,]+)', resultado)
        simple_barra_match = re.match(r'(\d+)/([\d,]+)', resultado)
        solo_numero_match = re.match(r'([\d,]+)', resultado)
        obs_tiempo_solo_match = re.match(r'(\d+)\((\d+) Obs - (\d+) Tpo\)', resultado)

        if i == 0:
            if simple_barra_match:
                ptos_obs[i] = int(simple_barra_match.group(1))
                tiempo[i] = float(simple_barra_match.group(2).replace(',', '.'))
            elif obs_tiempo_barra_match:
                ptos_obs[i] = int(obs_tiempo_barra_match.group(2))
                ptos_tiempo[i] = int(obs_tiempo_barra_match.group(3))
                tiempo[i] = float(obs_tiempo_barra_match.group(4).replace(',', '.'))
            elif solo_numero_match:
                ptos_tiempo[i] = float(solo_numero_match.group(0).replace(',', '.'))
            elif obs_tiempo_solo_match:
                ptos_obs[i] = int(obs_tiempo_solo_match.group(2))
                ptos_tiempo[i] = int(obs_tiempo_solo_match.group(3))
        elif i == 1:
            if obs_tiempo_barra_match:
                ptos_obs[i] = int(obs_tiempo_barra_match.group(2))
                ptos_tiempo[i] = int(obs_tiempo_barra_match.group(3))
                tiempo[i] = float(obs_tiempo_barra_match.group(4).replace(',', '.'))
            elif simple_barra_match:
                ptos_obs[i] = int(simple_barra_match.group(1))
                tiempo[i] = float(simple_barra_match.group(2).replace(',', '.'))
            elif obs_tiempo_solo_match:
                obs_tpo = re.match(r'(\d+)\((\d+) Obs - (\d+) Tpo\)', resultado)
                if obs_tpo:
                    ptos_obs[i] = int(obs_tpo.group(2))
                    ptos_tiempo[i] = int(obs_tpo.group(3))
        elif i == 2:
            if simple_barra_match:
                ptos_obs[i] = int(simple_barra_match.group(1))
                tiempo[i] = float(simple_barra_match.group(2).replace(',', '.'))

    return (ptos_obs[0], ptos_tiempo[0], tiempo[0],
            ptos_obs[1], ptos_tiempo[1], tiempo[1],
            ptos_obs[2], ptos_tiempo[2], tiempo[2])

def mergeo_dfs(ruta_df_concursos, ruta_df_pruebas, ruta_guardado_df_final):

    with open(ruta_df_concursos, 'r', encoding='utf-8') as file:
        datos_concursos = json.load(file)

    df_concursos = pd.DataFrame(datos_concursos)
    df_concursos = df_concursos.rename(columns = {"Nombre": "Concurso", "Categoría": "Categoria_concurso"})
    df_concursos["Concurso"] = df_concursos["Concurso"].str.strip()

    df_pruebas_resultados = pd.read_csv(ruta_df_pruebas, index_col=0)

    df_final = pd.merge(df_pruebas_resultados, df_concursos, on = "Concurso", how = "inner")
    df_final['Fecha_prueba'] = pd.to_datetime(df_final['Fecha_prueba'])
    df_final['Inicio'] = pd.to_datetime(df_final['Inicio'], dayfirst=True)
    df_final['Final'] = pd.to_datetime(df_final['Final'], dayfirst=True)
    df_final = df_final[(df_final['Fecha_prueba'] >= df_final['Inicio']) & (df_final['Fecha_prueba'] <= df_final['Final']) & (df_final["Categoria"] == df_final["Categoria_concurso"])]
    df_final = df_final.drop(['Puntuacion', 'Resultados', 'Categoria_concurso', 'Pais_jinete', 'Pais_caballo', 'Raza_caballo'], axis=1)
    df_final["Jinete"] = df_final["Jinete"].str.lower()
    df_final["Caballo"] = df_final["Caballo"].str.lower()
    df_final["Lic_jinete"] = df_final["Lic_jinete"].astype(str)
    df_final["Lic_caballo"] = df_final["Lic_caballo"].astype(str)
    # df_final["Raza_caballo"] = df_final["Raza_caballo"].apply(lambda x: None if x == '(Indt.)' else x)
    df_final["Lic_jinete"] = df_final["Lic_jinete"].apply(lambda x: "10186822" if x == '--' else x)
    df_final["Jinete"] = df_final["Jinete"].apply(lambda x: "jesus folch redondo" if x == '-- -- --' else x)
    lista = ["ELI", "RET", "NOP"]
    df_final["Posicion"] = df_final["Posicion"].apply(lambda x: None if x in lista else x)
    df_final["Lic_caballo"] = df_final["Lic_caballo"].apply(lambda x: None if x == '--' else x)

    lic_mas_larga_por_jinete = (
        df_final[["Jinete", "Lic_jinete"]]
        .drop_duplicates()
        .assign(longitud=lambda x: x["Lic_jinete"].astype(str).str.len())
        .sort_values("longitud", ascending=False)
        .drop_duplicates(subset="Jinete")
        .drop(columns="longitud")
        .set_index("Jinete")
    )

    lic_mas_larga_por_caballo = (
        df_final[["Caballo", "Lic_caballo"]]
        .drop_duplicates()
        .assign(longitud=lambda x: x["Lic_caballo"].astype(str).str.len())
        .sort_values("longitud", ascending=False)
        .drop_duplicates(subset="Caballo")
        .drop(columns="longitud")
        .set_index("Caballo")
    )

    # 2. Reemplazar en el DataFrame original
    df_final["Lic_jinete"] = df_final["Jinete"].map(lic_mas_larga_por_jinete["Lic_jinete"])
    df_final["Lic_caballo"] = df_final["Caballo"].map(lic_mas_larga_por_caballo["Lic_caballo"])

    df_final.to_csv(ruta_guardado_df_final)
    
# def extraccion_resultados_jinetes_caballos(driver, diccionario_jinetes, diccionario_caballos):

#     siguiente_prueba_1 = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[3]/div[6]/div/table/tbody/tr/td/a" # completo 
#     siguiente_prueba_2 = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[2]/div[6]/div/table/tbody/tr/td/a" # salto y doma                 
                        
#     while True:
#         try:
#             time.sleep(5)

#             # aqui iria descarga de resultados
#             even_rows = len(buscador_elementos(driver, "EvenRows", busqueda = "class_name", cantidad = False)) # salto nacional, completo nacional, salto internacional 
#             odd_rows = len(buscador_elementos(driver, "OddRows", busqueda = "class_name", cantidad = False)) # salto nacional, completo nacional, salto internacional 
#             rango = even_rows + odd_rows + 1
         
#             for j in range(1, rango):

#                 nombre_jinete = f"#A2_{j}_2"
#                 licencia_jinete = f"#A2_{j}_1"
                
#                 jinete = (buscador_elementos(driver, nombre_jinete, busqueda= "css_selector").text, buscador_elementos(driver, licencia_jinete, busqueda= "css_selector").text)
#                 jinetes_existentes = list(zip( diccionario_jinetes["Nombre"],
#                                                diccionario_jinetes["Licencia"] ))
                
#                 path_completo_jinete = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr[{j}]/td[3]/div/div/a"
                                       
#                 if jinete not in jinetes_existentes:
#                     time.sleep(3)
                    
#                     driver.refresh()
#                     time.sleep(3)
#                     buscador_elementos(driver, path_completo_jinete).click()
#                     time.sleep(7)        
#                     path_info_jinete = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[3]/div[2]/div/table/tbody/tr[2]/td[2]/table"
#                     informacion_jinete = buscador_elementos(driver, path_info_jinete).text.split("\n")
#                     if "Federación Extranjera" in informacion_jinete[7]:
#                         guardado_info(diccionario = diccionario_jinetes, elementos = informacion_jinete, federacion = "extranjera", info = "jinetes")                                    
#                     else:
#                         guardado_info(diccionario = diccionario_jinetes, elementos = informacion_jinete, federacion = "nacional", info = "jinetes")             
#                     driver.back()

#             for j in range(1, rango):
                
#                 nombre_caballo = f"#A2_{j}_4"
#                 licencia_caballo = f"#A2_{j}_3"

#                 caballo = (buscador_elementos(driver, nombre_caballo, busqueda = "css_selector").text, buscador_elementos(driver, licencia_caballo, busqueda = "css_selector").text)
#                 caballos_existentes = list(zip( diccionario_caballos["Nombre"],
#                                                diccionario_caballos["Licencia"] ))
                
#                 path_completo_caballo = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr[{j}]/td[5]/div/div/a"
                                          
#                 if caballo not in caballos_existentes:
#                     time.sleep(3)
#                     try:
#                         buscador_elementos(driver, path_completo_caballo).click() 
#                     except NoSuchElementException:
#                         driver.refresh()
#                         time.sleep(3)
#                         buscador_elementos(driver, path_completo_caballo).click()
#                     time.sleep(7)               
#                     path_info_caballo = "pos33"            
#                     informacion_caballo = buscador_elementos(driver, path_info_caballo, "class_name").text.split("\n")
#                     if "Federación Extranjera" in informacion_caballo[8]:
#                         guardado_info(diccionario = diccionario_caballos, elementos = informacion_caballo, federacion = "extranjera", info = "caballos")                                   
#                     else:
#                         guardado_info(diccionario = diccionario_caballos, elementos = informacion_caballo, federacion = "nacional", info = "caballos")  
#                     driver.back()
            
#             try:
#                 buscador_elementos(driver, siguiente_prueba_1).click()
#             except NoSuchElementException:
#                 buscador_elementos(driver, siguiente_prueba_2).click()

#             time.sleep(7)

#             try:
#                 WebDriverWait(driver, 5).until (EC.alert_is_present())
#                 # switch_to.alert for switching to alert and accept
#                 alert = driver.switch_to.alert
#                 print("alert Exists in page")
#                 alert.accept()            
#                 break
            
#             except TimeoutException:   
#                 print("alert does not Exist in page")
                
#         except Exception as e:
#             print("Error en el bucle:", e)
#             break

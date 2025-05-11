# Importamos las librerías necesarias
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
from src.soporte_extraccion_general import get_competiciones, cambio_pestaña, resultados_disciplina, buscador_elementos, guardado_info, competiciones_año, obtencion_año, creacion_dictios_guardado, extraccion_info_concursos, extraccion_info_pruebas, archivos

def extraccion_completo_nac(url, lista_rutas):

    dictio_concursos_completo_nac, dictio_pruebas_completo_nac = creacion_dictios_guardado()
    urls_resultados_completo_nac = []

    driver = get_competiciones(url, lista_rutas[0])
    time.sleep(2)

    # Seleccionamos el ambito de los concursos y la disciplina, en este caso nacional y completo
    ambito_buscado, disciplina_buscada = resultados_disciplina(driver, disciplina = "completo")
    cambio_pestaña(1,driver)
    time.sleep(2)

    año = obtencion_año(driver)

    while año >= 2017:

        # vamos a todos los concursos del año en el que estemos
        competiciones_año(driver)

        maximo_n_concursos = int(buscador_elementos(driver, "/html/body/form/div/div/div/ul/li[13]/font").text.split(" ")[-1].replace("(", "").replace(")", ""))
        if año == 2025:
            rango = range(5,21)
        elif año < 2025:
            rango = range(5, maximo_n_concursos + 5) 

        for i in rango:

            try:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/a")
                print(concurso_bueno.text)
                time.sleep(1)
                try:
                    concurso_bueno.click()
                    #cambio_pestaña(1, driver)
                    time.sleep(2)
                    contenido_general =  buscador_elementos(driver, "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table").text.split('\n')
                                                                    
                    if "Resultados: Ver resultados  Ver" not in contenido_general:
                        driver.back()
                        time.sleep(1)

                    elif "Resultados: Ver resultados  Ver" in contenido_general:
                        print(contenido_general)
                        
                        extraccion_info_concursos(driver, diccionario_concursos=dictio_concursos_completo_nac, ambito_buscado=ambito_buscado, contenido_general=contenido_general)
                        try:
                            cambio_pestaña(2, driver)
                            time.sleep(1)
                            extraccion_info_pruebas(driver, dictio_concursos_completo_nac, dictio_pruebas_completo_nac, urls_resultados_completo_nac)

                            driver.close()
                            cambio_pestaña(1, driver)
                            driver.back()
                            time.sleep(2)

                        except IndexError:
                            time.sleep(5)
                            driver.refresh()
                            try:
                                cambio_pestaña(2, driver)
                                time.sleep(1)
                                extraccion_info_pruebas(driver, dictio_concursos_completo_nac, dictio_pruebas_completo_nac, urls_resultados_completo_nac)
                            except Exception as e:
                                driver.close()
                                cambio_pestaña(1,driver)
                                driver.back()
                                time.sleep(1)

                except NoSuchElementException:
                    raise NoSuchElementException

            except NoSuchElementException:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/font").text
                print(concurso_bueno)

        lista_archivos = [dictio_concursos_completo_nac, dictio_pruebas_completo_nac, urls_resultados_completo_nac]
        nombres_archivos = archivos(disciplina_buscada, ambito_buscado, año)

        i = 0
        for ruta in lista_rutas:
                 
            with open(f"{ruta}{nombres_archivos[i]}.json", "w", encoding="utf-8") as f:
                         json.dump(lista_archivos[i], f, ensure_ascii=False, indent=4) # se deja la ruta desde la que estoy ejecutando .py, no desde el src
            i += 1

        buscador_elementos(driver,"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/a").click()        
        año = obtencion_año(driver)

    driver.quit()   

def extraccion_completo_int(url, lista_rutas):

    dictio_concursos_completo_int, dictio_pruebas_completo_int = creacion_dictios_guardado()
    urls_resultados_completo_int = []

    # inicializamos el driver y lo abrimos
    driver = get_competiciones(url, lista_rutas[0])
    time.sleep(2)

    # Seleccionamos el ambito de los concursos y la disciplina, en este caso nacional y completo
    ambito_buscado, disciplina_buscada = resultados_disciplina(driver, ambito = "internacional", disciplina = "completo")
    cambio_pestaña(1,driver)
    time.sleep(2)

    año = obtencion_año(driver)

    while año >= 2017:

        # Buscamos los concursos del año que nos aparece
        competiciones_año(driver)

        time.sleep(1)

        maximo_n_concursos = int(buscador_elementos(driver, "/html/body/form/div/div/div/ul/li[13]/font").text.split(" ")[-1].replace("(", "").replace(")", ""))
        if año == 2025:
            rango = range(5,33)
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

                        extraccion_info_concursos(driver, diccionario_concursos=dictio_concursos_completo_int, ambito_buscado=ambito_buscado, contenido_general=contenido_general)
                        time.sleep(1)
                        try:
                            cambio_pestaña(3,driver)
                            time.sleep(2)
                            extraccion_info_pruebas(driver, dictio_concursos_completo_int, dictio_pruebas_completo_int, urls_resultados_completo_int)
                            
                            driver.close()
                            cambio_pestaña(2, driver)
                            driver.close()
                            cambio_pestaña(1, driver)
                            time.sleep(2)

                        except IndexError:
                            time.sleep(5)
                            driver.refresh()
                            try:
                                extraccion_info_pruebas(driver, dictio_concursos_completo_int, dictio_pruebas_completo_int, urls_resultados_completo_int)
                                driver.close()
                                cambio_pestaña(1, driver)
                            except Exception as e:
                                driver.close()
                                cambio_pestaña(1, driver)
                                time.sleep(2)

                except NoSuchElementException:
                    raise NoSuchElementException

            except NoSuchElementException:
                concurso_bueno = buscador_elementos(driver,f"/html/body/form/div/div/div/div/div[13]/table/tbody/tr[{i}]/td[4]/font").text
                print(concurso_bueno)

        lista_archivos = [dictio_concursos_completo_int, dictio_pruebas_completo_int, urls_resultados_completo_int]
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

def extraccion_resultados_jinetes_caballos(lista_urls):

    diccionario_jinetes, diccionario_caballos = creacion_dictios_guardado(creacion = False)

    for url in lista_urls:

        driver = get_competiciones(url)

        siguiente_prueba_1 = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[3]/div[6]/div/table/tbody/tr/td/a" # completo 
        siguiente_prueba_2 = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[2]/div[6]/div/table/tbody/tr/td/a" # salto y doma                 

        while True:
            try:
                time.sleep(5)

                #  aqui iria descarga de resultados
                jinetes = len(buscador_elementos(driver, "pos91", busqueda = "class_name", cantidad = False)) # salto nacional, completo nacional, salto internacional 
                for j in range(1, jinetes + 1):

                    path_completo_jinete = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div[2]/div/table/tbody/tr[{j}]/td/div/table/tbody/tr[1]/td/div/div[3]/div/table/tbody/tr/td/a"
                    path_completo_licencia = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div[2]/div/table/tbody/tr[{j}]/td/div/table/tbody/tr[1]/td/div/div[2]/div/table/tbody/tr/td/div"
                    
                    jinete = (buscador_elementos(driver, path_completo_jinete).text, buscador_elementos(driver, path_completo_licencia).text)
                    jinetes_existentes = list(zip( diccionario_jinetes["Nombre"],
                                                diccionario_jinetes["Licencia"] ))

                    if jinete not in jinetes_existentes:
                        buscador_elementos(driver, path_completo_jinete).click()
                        time.sleep(7)        
                        path_info_jinete = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[3]/div[2]/div/table/tbody/tr[2]/td[2]/table"
                        informacion_jinete = buscador_elementos(driver, path_info_jinete).text.split("\n")
                        if "Federación Extranjera" in informacion_jinete[7]:
                            guardado_info(diccionario = diccionario_jinetes, elementos = informacion_jinete, federacion = "extranjera", info = "jinetes")                                    
                        else:
                            guardado_info(diccionario = diccionario_jinetes, elementos = informacion_jinete, federacion = "nacional", info = "jinetes")             
                        driver.back()

                caballos = len(buscador_elementos(driver, "pos101", busqueda = "class_name", cantidad = False)) # salto nacional, completo nacional, salto internacional 
                for j in range(1, caballos + 1):

                    path_completo_caballo = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div[2]/div/table/tbody/tr[{j}]/td/div/table/tbody/tr[1]/td/div/div[5]/div/table/tbody/tr/td/a"
                    path_completo_licencia = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div[2]/div/table/tbody/tr[{j}]/td/div/table/tbody/tr[1]/td/div/div[4]/div/table/tbody/tr/td/div"

                    caballo = (buscador_elementos(driver, path_completo_caballo).text, buscador_elementos(driver, path_completo_licencia).text)
                    caballos_existentes = list(zip( diccionario_caballos["Nombre"],
                                                diccionario_caballos["Licencia"] ))
                    
                    if caballo not in caballos_existentes:
                        buscador_elementos(driver, path_completo_caballo).click() 
                        time.sleep(7)                                  
                        informacion_caballo = buscador_elementos(driver, "pos35", busqueda= "class_name").text.split("\n")
                        if "Federación Extranjera" in informacion_caballo[8]:
                            guardado_info(diccionario = diccionario_caballos, elementos = informacion_caballo, federacion = "extranjera", info = "caballos")                                   
                        else:
                            guardado_info(diccionario = diccionario_caballos, elementos = informacion_caballo, federacion = "nacional", info = "caballos")  
                        driver.back()
                
                try:
                    buscador_elementos(driver, siguiente_prueba_1).click()
                except NoSuchElementException:
                    buscador_elementos(driver, siguiente_prueba_2).click()

                time.sleep(7)

                try:
                    WebDriverWait(driver, 5).until (EC.alert_is_present())
                    # switch_to.alert for switching to alert and accept
                    alert = driver.switch_to.alert
                    print("alert Exists in page")
                    alert.accept()            
                    break
                
                except TimeoutException:   
                    print("alert does not Exist in page")
                    
            except Exception as e:
                print("Error en el bucle:", e)
                break

        driver.quit()


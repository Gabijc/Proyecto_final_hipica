# Importamos las librerías necesarias
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from src.soporte_extraccion_general import cambio_pestaña, buscador_elementos, guardado_info

def extraccion_resultados_jinetes_caballos(driver, diccionario_jinetes, diccionario_caballos):

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

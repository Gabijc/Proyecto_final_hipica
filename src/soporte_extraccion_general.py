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
import os
from selenium.webdriver.chrome.options import Options

def get_competiciones(url):
    """
    Función que abre una nueva ventana de Chrome en la URL indicada y devuelve el driver.

    Args:
        url (str): URL sobre la que se quiere realizar el scrapeo de información.

    Returns:
        Webdriver.Chrome: Instancia del navegador abierto en la URL proporcionada.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def creacion_dictios_guardado():

    dictio_concursos = {'Nombre': [],
                        'Categoría': [],
                        'Provincia': [],
                        'Localidad': [],
                        'Disciplina': [],
                        'Federación': [],
                        'Resultados': [],
                        'País': []}
    
    dictio_pruebas = {'Disciplina': [],
                            'Fecha': [],
                            'Prueba': [],
                            'Categoría': [],
                            'Número': [],
                            'Concurso': []}
    
    dictio_jinetes = { "Nombre": [],
                       "Licencia": [],
                       "Sexo": [],
                       "País": [],
                       "Federación": [],
                       "Disciplina": []}
    
    dictio_caballos = {"Nombre": [],
                        "Licencia": [],
                        "Edad": [],
                        "País": [],
                        "Raza": [],
                        "Sexo": [],
                        "Federación": [],
                        "Disciplina": []}
    
    return dictio_concursos, dictio_pruebas, dictio_jinetes, dictio_caballos


# definimos la función que nos permitirá movernos por las pestañas que se van abriendo según navegamos por la página
def cambio_pestaña(nº_pestaña, navegador):
    """
    Función que navega por las pestañas abiertas en el navegador.

    Args:
        nº_pestaña (int): Índice de la pestaña a la que se quiere cambiar (empezando desde 0).
        navegador (webdriver.Chrome): Instancia del navegador web abierta con Selenium.
    
    Returns:
        Cambio a la pestaña indicada. 
    """
    pestañas = navegador.window_handles  # Lista de pestañas abiertas
    return navegador.switch_to.window(pestañas[nº_pestaña])  # Cambia a la pestaña que se le indique




def resultados_disciplina(driver, ambito = "nacional", disciplina = "salto"):

    wait = WebDriverWait(driver, 5)

    disciplinas = ["salto", "completo", "doma"]

    if disciplina not in disciplinas:
        raise ValueError(f"El ámbito {ambito} no es válido, por favor ingrese otro.")

    elif disciplina in disciplinas:

        if ambito == "nacional":
            if disciplina == "salto":
                concursos = "/html/body/div[3]/div[2]/div/section/article/span/ul[1]/li[3]/strong/a"

            elif disciplina == "completo":
                concursos = "/html/body/div[3]/div[2]/div/section/article/span/ul[3]/li[2]/strong/a"

            elif disciplina == "doma":
                concursos = "/html/body/div[3]/div[2]/div/section/article/span/ul[2]/li[2]/strong/a"

        elif ambito == "internacional":
            
            if disciplina == "salto":
                concursos = "/html/body/div[3]/div[2]/div/section/article/span/ul[1]/li[4]/strong/a"

            elif disciplina == "completo":
                concursos = "/html/body/div[3]/div[2]/div/section/article/span/ul[3]/li[3]/strong/a"

            elif disciplina == "doma":
                concursos = "/html/body/div[3]/div[2]/div/section/article/span/ul[2]/li[3]/strong/a"
              
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, concursos))).click()
            # Nos vamos a la pestaña de competiciones
            cambio_pestaña(1,driver)
            return ambito, disciplina
        except (TimeoutException, NoSuchElementException) as e:
            print(f"No se han encontrado las competiciones {ambito} de la disciplina {disciplina}. Error: {e}")
            return None, None



def obtencion_año(driver):

    path_año = "/html/body/form/table/tbody/tr[1]/td"
    año = int(buscador_elementos(driver, path_año).text.split(" ")[1])
    return año


def competiciones_año(driver):

    path_competiciones_año = '/html/body/form/div/div/div/ul/li[13]'
    comp_año = buscador_elementos(driver, path_competiciones_año).click()
    return comp_año


def guardado_info(diccionario,  elementos, claves = None, indices = None, default = None, step = None, guardado = True, info = None, federacion = None, ambito = None):
    
    info_disponible = ["general","concursos", "jinetes", "caballos"]

    if info not in info_disponible:
        raise ValueError(f"La información seleccionada no está disponible.")
    else:

        if info == "concursos":
            
            if ambito == "nacional":
                diccionario["Nombre"].append(elementos[0].split(":")[1].lstrip())
                diccionario["Categoría"].append(elementos[1].split(":")[1].lstrip())
                diccionario["Provincia"].append(elementos[2].split(":")[1].lstrip())
                diccionario["Localidad"].append(elementos[3].split(":")[1].lstrip())
                diccionario["Disciplina"].append(elementos[4].split(":")[1].lstrip())
                diccionario["Federación"].append(elementos[6].split(":")[1].lstrip())
                diccionario["Resultados"].append(elementos[-1].split(":")[1][0:4].lstrip())
                diccionario["País"].append("España")

            elif ambito == "internacional":
                diccionario["Nombre"].append(elementos[0].split(":")[1].lstrip())
                diccionario["Categoría"].append(elementos[1].split(":")[1].lstrip())
                diccionario["Provincia"].append(elementos[2].split(":")[1].lstrip())
                diccionario["Localidad"].append(elementos[3].split(":")[1].lstrip())
                diccionario["Disciplina"].append(elementos[4].split(":")[1].lstrip())
                diccionario["Federación"].append(elementos[6].split(":")[1].lstrip())
                diccionario["Resultados"].append(elementos[-1].split(":")[1][0:4].lstrip())
                diccionario["País"].append("España")

        elif info == "jinetes":

            if federacion == "extranjera":
                nombre = elementos[1].split("(")[0].strip()
                licencia = elementos[3]
                sexo = None
                pais = elementos[1].split("(")[1].strip(")")
                federacion = elementos[7]
                disciplina = elementos[-1]

            elif federacion == "nacional":
                nombre = elementos[1]
                licencia = elementos[3]
                sexo = elementos[5]
                pais = "ESP"
                federacion = elementos[7]
                disciplina = elementos[-1]
            
            jinete = (nombre, licencia, sexo, pais, federacion, disciplina)
            jinetes_existentes = list(zip(diccionario["Nombre"],
                                            diccionario["Licencia"],
                                            diccionario["Sexo"],
                                            diccionario["País"],
                                            diccionario["Federación"],
                                            diccionario["Disciplina"]))
            if jinete not in jinetes_existentes:
                diccionario["Nombre"].append(nombre)
                diccionario["Licencia"].append(licencia)
                diccionario["Sexo"].append(sexo)
                diccionario["País"].append(pais)
                diccionario["Federación"].append(federacion)
                diccionario["Disciplina"].append(disciplina)

        elif info == "caballos":
            if federacion == "extranjera":
                nombre = elementos[1].split("(")[0].strip()
                licencia = elementos[1].split("(")[2].strip().strip(")")
                edad = None
                raza = elementos[4]
                pais = elementos[1].split("(")[1].strip().strip(")")
                sexo = elementos[6]
                federacion = elementos[8]
                disciplina = elementos[-1]
                                
            elif federacion == "nacional":
                nombre = elementos[1].split("(")[0].strip().strip(")")
                licencia = elementos[1].split("(")[1].strip().strip(")")
                edad = elementos[3].split("(")[0].strip()
                raza = elementos[5]
                pais = "ESP"
                sexo = elementos[7]
                federacion = elementos[8]
                disciplina = elementos[-1]

            caballo = (nombre, licencia, edad, raza, sexo, pais, federacion, disciplina)
            caballos_existentes = list(zip(diccionario["Nombre"],
                                            diccionario["Licencia"],
                                            diccionario["Edad"],
                                            diccionario["Raza"],
                                            diccionario["País"],
                                            diccionario["Sexo"],
                                            diccionario["Federación"],
                                            diccionario["Disciplina"]))
            
            if caballo not in caballos_existentes:
                diccionario["Nombre"].append(nombre)
                diccionario["Licencia"].append(licencia)
                diccionario["Edad"].append(edad)
                diccionario["Raza"].append(raza)
                diccionario["País"].append(pais)
                diccionario["Sexo"].append(sexo)
                diccionario["Federación"].append(federacion)
                diccionario["Disciplina"].append(disciplina)

        elif info == "general":

            for clave, indice in zip(claves, indices):
                    if guardado == True:  

                        if indice is not None and indice < len(elementos):
                            diccionario[clave].append(elementos[indice])

                        elif indice is None:    
                            diccionario[clave].append(default)

                    elif guardado == False:
                        if step is not None:
                            diccionario[clave].extend(elementos[indice::step])


def buscador_elementos(driver, elemento, busqueda = "path", cantidad = True):

    tipo_busqueda = { "path": By.XPATH,
                      "css_selector": By.CSS_SELECTOR,
                    "class_name": By.CLASS_NAME}
    
    if busqueda not in tipo_busqueda:
        raise ValueError(f"El tipo de busqueda metido no existe, seleccione uno de entre los siguientes: {list(tipo_busqueda.keys())}")
    
    metodo = tipo_busqueda[busqueda]
    
    if cantidad is True:
        return driver.find_element(metodo, elemento)

    elif cantidad is False:
        return driver.find_elements(metodo, elemento)
    
    else: 
        raise ValueError(f"No se pueden buscar más métodos.")
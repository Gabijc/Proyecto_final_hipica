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
import glob
import json
# from seleniumbase import Driver


def get_competiciones(url, ruta_carpeta_guardado):
    """
    Función que abre una nueva ventana de Chrome en la URL indicada y devuelve el driver.

    Args:
        url (str): URL sobre la que se quiere realizar el scrapeo de información.

    Returns:
        Webdriver.Chrome: Instancia del navegador abierto en la URL proporcionada.
    """

    download_dir = os.path.abspath(ruta_carpeta_guardado)
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    prefs = { "download.default_directory": download_dir,
              "download.prompt_for_download": False,
              "directory_upgrade": True,
              "safebrowsing.enabled": True }

    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options = chrome_options) 
    
    driver.get(url)
    return driver


def creacion_dictios_guardado(creacion = True):
    if creacion == True:
        dictio_concursos = {'Nombre': [],
                            'Categoría': [],
                            'Provincia': [],
                            'Localidad': [],
                            'Disciplina': [],
                            'Federación': [],
                            'Resultados': [],
                            'País': [], 
                            "Inicio": [],
                            "Final": [],
                            "Ambito": []}
        
        dictio_pruebas = {'Disciplina': [],
                                'Fecha': [],
                                'Prueba': [],
                                'Categoría': [],
                                'Número': [],
                                'Concurso': []}
        
        return dictio_concursos, dictio_pruebas
    
    elif creacion == False: 
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
        
        return dictio_jinetes, dictio_caballos


# definimos la función que nos permitirá movernos por las pestañas que se van abriendo según navegamos por la página
def cambio_pestaña(nº_pestaña, driver):
    """
    Función que navega por las pestañas abiertas en el navegador.

    Args:
        nº_pestaña (int): Índice de la pestaña a la que se quiere cambiar (empezando desde 0).
        navegador (webdriver.Chrome): Instancia del navegador web abierta con Selenium.
    
    Returns:
        Cambio a la pestaña indicada. 
    """
    driver.switch_to.window(driver.window_handles[nº_pestaña])


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
                diccionario["País"].append("Epaña")

            elif ambito == "internacional":
                try:
                    diccionario["Nombre"].append(elementos[0].split(":")[1].split("(")[0].strip())
                except IndexError:
                    diccionario["Nombre"].append(elementos[0].split(":")[1].lstrip())

                diccionario["Categoría"].append(elementos[1].split(":")[1].lstrip())
                diccionario["Provincia"].append(None)
                diccionario["Localidad"].append(elementos[3].split(":")[1].lstrip())
                diccionario["Disciplina"].append(elementos[4].split(":")[1].lstrip())
                diccionario["Federación"].append("Federación extranjera")
                diccionario["Resultados"].append(elementos[-1].split(":")[1][0:4].lstrip())
                diccionario["País"].append(elementos[2].split(":")[1].lstrip())

        elif info == "jinetes":

            if federacion == "extranjera":
                nombre = elementos[1].split("(")[0].strip()
                licencia = str(elementos[3])
                sexo = None
                pais = elementos[1].split("(")[1].strip(")")
                federacion = elementos[7]
                disciplina = elementos[-1]

            elif federacion == "nacional":
                nombre = elementos[1]
                licencia = str(elementos[3])
                sexo = elementos[5]
                pais = "ESP"
                federacion = elementos[7]
                disciplina = elementos[-1]
            

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
                edad = int(elementos[3].split("(")[0].strip())
                raza = elementos[5]
                pais = "ESP"
                sexo = elementos[7]
                federacion = elementos[8]
                disciplina = elementos[-1]

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
    
def extraccion_info_concursos(driver, diccionario_concursos, ambito_buscado, contenido_general):

    # Guardamos la información del concurso en el diccionario creado
    guardado_info(diccionario_concursos, contenido_general, info="concursos", ambito=ambito_buscado)

    # Lista de paths posibles según el ámbito
    if ambito_buscado == "nacional":
        paths_botones = [ "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[20]/td[3]/a",
                          "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[18]/td[3]/a",
                          "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[16]/td[3]/a",
                          "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[19]/td[3]/a",
                          "/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[21]/td[3]/a"]
        
    elif ambito_buscado == "internacional":
        paths_botones = ["/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[18]/td[3]/a",
                         "/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[21]/td[3]/a",
                         "/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[16]/td[3]/a",
                         "/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[19]/td[3]/a",
                         "/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[20]/td[3]/a"]
    else:
        print(f"Ámbito '{ambito_buscado}' no reconocido.")
        return

    # Intentamos hacer clic en los paths en orden
    clicked = False
    for path in paths_botones:
        try:
            boton = buscador_elementos(driver, path)
            boton.click()
            clicked = True
            break  # Si hace clic con éxito, salimos del bucle
        except NoSuchElementException:
            continue  # Si falla, probamos el siguiente

    if not clicked:
        print("No se pudo hacer clic en ninguno de los botones de pruebas.")

        

def extraccion_info_pruebas(driver, diccionario_concursos, diccionario_pruebas, lista_urls):
    
    # Obtenemos la información del concurso que se encuentra en la tabla de las pruebas
    path_info_restante = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[3]/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td"
                          
    info_concurso_restante = buscador_elementos(driver, path_info_restante).text.split("\n")

    # metemos la info del concurso que nos falta
    guardado_info(diccionario = diccionario_concursos, elementos = info_concurso_restante, claves = ["Inicio", "Final", "Ambito"], indices = [3, 5, -1], info = "general")

    # Obtenemos el nombre del concurso para luego meterlo en la tabla de pruebas
    path_nombre_concurso = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[3]/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr"
    nombre_concurso = buscador_elementos(driver, path_nombre_concurso).text.strip()

    # Obtenemos las pruebas del concurso
    path_pruebas = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]"
    pruebas = buscador_elementos(driver, path_pruebas).text.split("\n")
                
    claves_pruebas = list(diccionario_pruebas.keys())
    guardado_info(diccionario = diccionario_pruebas, elementos = pruebas, claves = claves_pruebas, indices = [6, 7, 8, 9, 10], step = 6, guardado = False, info = "general")

    numero_pruebas = len(pruebas[6::6])  # Asumimos que 'Disciplina' tiene una fila por prueba
    diccionario_pruebas["Concurso"].extend([nombre_concurso] * numero_pruebas)

    # accedemos a los resultados de la primera prueba
    path_resultados_pruebas = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[2]/div[2]/div/table/tbody/tr/td/div/div/table/tbody/tr[1]/td/div/div/table/tbody/tr[1]/td/div/div[3]/div/table/tbody/tr/td/a"
    try:
        buscador_elementos(driver, path_resultados_pruebas).click()
        time.sleep(4)
                
        url = driver.current_url
        lista_urls.append(url)
        
    except Exception as e:
        print(f"Error al acceder a los resultados as {e}")


def archivos(disciplina, ambito, año):
    concursos = f"concursos_{disciplina}_{ambito}_{año}"
    pruebas = f"pruebas_{disciplina}_{ambito}_{año}"
    urls = f"urls_{disciplina}_{ambito}_{año}"
    lista_nombres_archivos = [concursos, pruebas]
    return lista_nombres_archivos

def descargar_excel(lista_urls, ruta_guardado, disciplina):
  
  if disciplina == "salto": 
    i = 5
    j = 3
  elif disciplina == "doma":
    i = 4
    j = 3
  elif disciplina == "completo":
    i = 3
    j = 4

  selector_enlace_excel = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[{j}]/div[1]/div/table/tbody/tr/td/a"
  ruta_nombre_prueba = f"/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[{i}]/div[2]/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td"
  siguiente_prueba_1 = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[3]/div[6]/div/table/tbody/tr/td/a" # completo 
  siguiente_prueba_2 = "/html/body/form/table/tbody/tr/td/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/div[1]/div[2]/div[2]/div[6]/div/table/tbody/tr/td/a" # salto y doma 
  

  for url in lista_urls:

    driver = get_competiciones(url, ruta_guardado)
    time.sleep(2)
    try: 

      while True:

        try:
            
          coso = buscador_elementos(driver, ruta_nombre_prueba).text
          print(coso)
          buscador_elementos(driver, selector_enlace_excel).click()
          print(f"Descarga del archivo Excel iniciada. Se guardará en: {ruta_guardado}")
          time.sleep(8) # Espera a que la descarga se complete (ajusta según sea necesario)

          archivos_en_ruta = glob.glob(os.path.join(ruta_guardado, '*.xls'))  # Lista de archivos .xls en la carpeta de descargas
          print(f"Archivos encontrados en la ruta: {os.listdir(ruta_guardado)}")
            
          if archivos_en_ruta:
            time.sleep(1)
          else:
              print("No se encontraron archivos .xls en la carpeta de descarga.")

        except Exception as e:
            print(f"Ocurrió un error: {e}")
        
        try:
          buscador_elementos(driver, siguiente_prueba_1).click()
        except NoSuchElementException:
          buscador_elementos(driver, siguiente_prueba_2).click()

        time.sleep(3)

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

    finally:
      driver.quit()

def lectura_excels(ruta_archivo):

    directorio = ruta_archivo

    # Obtener la lista de todos los archivos en el directorio
    archivos = os.listdir(directorio)

    # Filtrar solo los archivos que parecen ser de Excel (puedes refinar esto más si es necesario)
    archivos_excel = [f for f in archivos if f.endswith(('.xlsx', '.xls'))]

    if archivos_excel:
        # Ordenar la lista de archivos para asegurar que el "primero" sea consistente
        archivos_excel.sort()

        for nombre_excel in archivos_excel:
            ruta_excel = os.path.join(directorio, nombre_excel)
            print(f"\n--- Leyendo archivo: {nombre_excel} ---")
            try:
                # Leer el archivo Excel actual
                df = pd.read_excel(ruta_excel)
                print(df.head()) # Mostrar las primeras filas de cada DataFrame
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo: {ruta_excel}")
            except Exception as e:
                print(f"Ocurrió un error al leer el archivo {nombre_excel}: {e}")
    else:
        print("No se encontraron archivos Excel en el directorio.")            
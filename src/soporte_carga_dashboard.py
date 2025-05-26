import streamlit as st  # type: ignore
import pandas as pd
import psycopg2 as ps  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import numpy as np
import re
from datetime import date
import os
from dotenv import load_dotenv  # type: ignore


load_dotenv()

dbname = os.getenv("nombre_BBDD")
user = os.getenv("usuario")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

def conexion_BBDD(nombre_BBDD, usuario, contraseña, anfitrion, puerto):

    conn = ps.connect(
                    dbname = nombre_BBDD, 
                    user = usuario,
                    password = contraseña,
                    host = anfitrion,
                    port = puerto)

    return conn

conn = conexion_BBDD(dbname, user, password, host, port)
cur = conn.cursor()


meses = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril"
}

def ejecutor_querys(cur, query):
    cur.execute(query)
    return cur.fetchall()


def concursos_seleccionado(elementos, coso = 'info_concursos'):
    
    if coso == "info_concursos":
        if not elementos:
                return pd.DataFrame()
        concursos_str = ', '.join([f"'{c}'" for c in elementos])
        query = f""" 
                SELECT 
                    c.nombre_concurso,
                    p.nombre_prueba,
                    p.fecha_prueba
                FROM resultados r
                JOIN pruebas p ON r.id_prueba = p.id_prueba
                JOIN concursos c ON r.id_concurso = c.id_concurso
                WHERE c.nombre_concurso IN ({concursos_str})
                GROUP BY c.nombre_concurso, p.nombre_prueba, p.fecha_prueba
                ORDER BY 3;
        """
        return pd.DataFrame(ejecutor_querys(cur, query))
    
    elif coso == "jinetes":
        query = f""" 
            SELECT 
                DISTINCT c.nombre_caballo
            FROM resultados r
                JOIN caballos c ON r.id_caballo = c.id_caballo
                JOIN jinetes j ON r.id_jinete = j.id_jinete
            WHERE j.nombre_jinete = '{elementos}';
        """
        return pd.DataFrame(ejecutor_querys(cur, query))

def extraer_altura_y_edad(texto):
    altura = None
    edad = None

    match_altura = re.search(r'(\d{1,2}[,.]\d{2})\s?(?:m\.?)?', texto)
    if match_altura:
        altura = match_altura.group(1).replace(',', '.')

    match_edad = re.search(r'\b([5-8])\s?años\b', texto, flags=re.IGNORECASE)
    if match_edad:
        edad = f"{match_edad.group(1)} años"

    return altura, edad

def redondear_a_multiplo(valor, multiplo):
        return int(round(valor / multiplo) * multiplo)

def info_jinete_caballo(jinete_entrada, caballo_entrada):
    if "'" in caballo_entrada:
        caballo_entrada = caballo_entrada.replace("'", "''")
    query_prueba = f""" 
            SELECT 
                j.nombre_jinete,
                c.nombre_caballo,
                rs.puntos_obs_r1,
                rs.puntos_tmp_r1,
                rs.tiempo_r1,
                rs.puntos_obs_r2,
                rs.puntos_tmp_r2,
                rs.tiempo_r2,
                rs.puntos_obs_r3,
                rs.puntos_tmp_r3,
                rs.tiempo_r3,
                p.nombre_prueba,
                co.nombre_concurso,
                r.estado,
                p.fecha_prueba,
                r.puesto,
                co.id_concurso
            FROM resultados r
                JOIN caballos c ON r.id_caballo = c.id_caballo
                JOIN jinetes j ON r.id_jinete = j.id_jinete
                JOIN resultados_salto rs ON r.id_resultado = rs.id_resultado
                JOIN pruebas p ON r.id_prueba = p.id_prueba
                JOIN concursos co ON r.id_concurso = co.id_concurso
            WHERE j.nombre_jinete = '{jinete_entrada}' AND c.nombre_caballo = '{caballo_entrada}';
    """
    binomio = pd.DataFrame(ejecutor_querys(cur, query_prueba)).rename(columns = {0: 'jinete', 1: 'caballo', 2: 'puntos_obs_r1', 3: 'puntos_tmp_r1', 4: 'tiempo_r1',
                                                                    5: 'puntos_obs_r2', 6: 'puntos_tmp_r2', 7: 'tiempo_r2',
                                                                    8: 'puntos_obs_r3', 9: 'puntos_tmp_r3', 10: 'tiempo_r3',
                                                                    11: 'prueba', 12: 'concurso', 13: 'estado', 14: 'fecha_prueba', 15: 'puesto', 16: 'id_concurso'}).drop_duplicates()
    # METRICAS
    n_concursos = len(binomio['id_concurso'].unique()) # numero de concursos en los que el caballo ha competido con el jinete seleccionado
    # n_caballos_corridos = len(caballos) # numero de cabllos que el jinete seleccionado corre actualmente/ha corrido este año
    porcentaje_recorridos_finalizados = round(len(binomio[binomio["estado"] == "FIN"])/len(binomio) * 100, 2) # porcentaje de pruebas finalizadas

    tipos_pruebas_altura = binomio['prueba'].apply(extraer_altura_y_edad)
    alturas = []
    edad = []
    for elemento in tipos_pruebas_altura:
        if pd.notna(elemento[0]):
            alturas.append(elemento[0])
        if pd.notna(elemento[1]):
            edad.append(elemento[1])
        else:
            continue
    alturas_buenas = list(set(alturas)) # alturas en las que el jinete ha competido con el caballo seleccionado
    edad_bueno = list(set(edad)) # si es caballo joven o no 


    tiempos = binomio[['tiempo_r1', 'tiempo_r2', 'tiempo_r3']].apply(pd.to_numeric, errors='coerce')
    promedio_tiempo = round(tiempos.stack().mean(), 2) # promedio de tiempo que realiza el caballo en un recorrido

    # Solo filas con estado FIN (salida a pista válida)
    df_fin = binomio[binomio['estado'] == 'FIN']

    # Vamos a revisar todas las rondas para contar las salidas y calcular puntos
    rondas = ['r1', 'r2', 'r3']

    # Creamos listas para guardar resultados de cada salida a pista (cada ronda válida)
    salidas_pista = []

    for _, fila in df_fin.iterrows():
        for r in rondas:
            p_obs = fila[f'puntos_obs_{r}']
            p_tmp = fila[f'puntos_tmp_{r}']
            tiempo = fila[f'tiempo_{r}']
            
            # Comprobar si salió a pista: alguna de estas 3 columnas tiene un valor numérico válido
            if pd.notna(p_obs) or pd.notna(p_tmp) or pd.notna(tiempo):
                # Asegurarnos que p_obs sea número, sino 0 para contar correctamente
                p_obs_val = p_obs if pd.notna(p_obs) else 0
                salidas_pista.append(p_obs_val)

    # Número de salidas a pista
    num_salidas = len(salidas_pista) # numero de recorridos/salidas a pista que ha realizado el cabllo con el jinete seleccionado

    # Promedio de puntos en obstáculos por salida (manejo seguro de NaN)
    if salidas_pista and not np.isnan(np.nanmean(salidas_pista)):
        media_real = np.nanmean(salidas_pista)
        promedio_puntos_obs = redondear_a_multiplo(media_real, 4)
    else:
        promedio_puntos_obs = "No hay datos"  # Puedes poner np.nan si prefieres indicar que no hay datos

    # Porcentaje de salidas con 0 puntos en obstáculos
    veces_cero = sum(1 for x in salidas_pista if x == 0) # numero de veces que el caballo ha hecho cero puntos en obstaculos
    promedio_veces_cero = (veces_cero / num_salidas if num_salidas > 0 else np.nan)*100
    jinete = binomio['jinete'].unique()[0]
    caballo = binomio['caballo'].unique()[0]
    edad_caballo = edad_bueno[0] if edad_bueno else "No joven"
    
    return jinete, caballo, edad_caballo, n_concursos, alturas_buenas, promedio_puntos_obs, promedio_veces_cero, binomio

def graficos_provincias (provincia, grafico_buscado, filtro = None):

    if grafico_buscado == 'ambitos':
        query_concursos_ambito_provincia = f"""

                WITH seleccion_provincia AS (
                    SELECT *
                    FROM concursos
                    WHERE provincia_concurso = '{provincia}'
                )
                SELECT 
                    ambito_concurso,
                    CONCAT((COUNT(id_concurso)) * 100 / (SELECT COUNT(id_concurso) FROM seleccion_provincia), ' ', '%')
                FROM seleccion_provincia
                GROUP BY ambito_concurso
                ORDER BY COUNT(id_concurso) DESC;
        """
        df = pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia))
        df[1] = df[1].str.replace('%', '').str.strip().astype(int)
        colores = ['#4c78a8', '#54a24b']
        fig2 = px.pie(df, values=1, names=0, title='Porcentaje de concursos por ámbito', color_discrete_sequence=colores)
        fig2.update_traces(textinfo='percent', textfont_color='white')
        fig2.update_layout(width=600, 
                                    height=400, 
                                    title_x=0.5, 
                                    title_font=dict(size=16, weight='bold'))
        st.plotly_chart(fig2, use_container_width=True)

    elif grafico_buscado == 'temporal':
        query_concursos_ambito_provincia = f"""
                WITH seleccion_provincia AS (
                    SELECT *
                    FROM concursos
                    WHERE provincia_concurso = '{provincia}'
                )
                SELECT 
                        EXTRACT(MONTH FROM fecha_inicio_concurso),
                        COUNT(id_concurso)
                FROM seleccion_provincia
                GROUP BY EXTRACT(MONTH FROM fecha_inicio_concurso)
                ORDER BY COUNT(id_concurso) DESC;
        """
        df = pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia)).sort_values(by=0, ascending=True)
        df[0] = df[0].apply(lambda x: meses[int(x)])
        fig1 = px.bar(df, x=0, y=1, title='Concursos por mes')
        fig1.update_traces(width=0.2)
        fig1.update_layout(
                width=800, 
                height=400,
                title_font=dict(size = 15, weight='bold'),
                title_x=0.5,
                xaxis_title=dict(text='Provincia', font=dict(size = 12, weight='bold')),
                yaxis_title=dict(text='Nº concursos', font=dict(size = 12, weight='bold'))
            )
        st.plotly_chart(fig1, use_container_width=True)

    elif grafico_buscado == 'localidades':
        query_concursos_ambito_provincia = f"""
                WITH seleccion_provincia AS (
                    SELECT *
                    FROM concursos
                    WHERE provincia_concurso = '{provincia}'
                )
                SELECT 
                        DISTINCT s.localidad_concurso,
                        COUNT(DISTINCT s.id_concurso),
                        SUM(r.dinero_premio)
                FROM seleccion_provincia s
                    JOIN resultados r on s.id_concurso = r.id_concurso
                GROUP BY DISTINCT localidad_concurso;
        """
        df = pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia)).rename(columns={0: 'Localidad', 1: 'Nº concursos', 2: 'Dinero repartido'})
        df["Dinero repartido"] = df["Dinero repartido"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €")
        return df
    
    elif grafico_buscado == 'categorias':
        query_concursos_ambito_provincia = f"""
                WITH seleccion_provincia AS (
                    SELECT *
                    FROM concursos
                    WHERE provincia_concurso = '{provincia}'
                )
                SELECT 
                        DISTINCT s.categoria_concurso,
                        COUNT( DISTINCT s.id_concurso),
                        SUM(r.dinero_premio),
                        COUNT(DISTINCT (r.id_jinete, r.id_caballo))
                FROM seleccion_provincia s
                    JOIN resultados r on s.id_concurso = r.id_concurso
                GROUP BY DISTINCT s.categoria_concurso;
        """

        if filtro == 'Concursos por categoría':
            # return pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia))
            fig = px.bar(pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia)), x = 0, y = 1, title = "Concursos por categoria")
            fig.update_layout(
                                        width=800, 
                                        height=400,
                                        title_font=dict(size = 15, weight='bold'),
                                        title_x=0.5,
                                        xaxis_title=dict(text='Categoría', font=dict(size = 12, weight='bold')),
                                        yaxis_title=dict(text='Nº concursos', font=dict(size = 12, weight='bold')))
            st.plotly_chart(fig, use_container_width=True)

        if filtro == 'Dinero por categoría':
            # return pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia))
            fig = px.bar(pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia)), x = 0, y = 2, title = "Concursos por categoria")
            fig.update_layout(
                                        width=800, 
                                        height=400,
                                        title_font=dict(size = 15, weight='bold'),
                                        title_x=0.5,
                                        xaxis_title=dict(text='Categoría', font=dict(size = 12, weight='bold')),
                                        yaxis_title=dict(text='Dinero repartido', font=dict(size = 12, weight='bold')))
            st.plotly_chart(fig, use_container_width=True)

        if filtro == 'Binomios por categoría':
            # return pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia))
            fig = px.bar(pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia)), x = 0, y = 3, title = "Concursos por categoria")
            fig.update_layout(
                                        width=800, 
                                        height=400,
                                        title_font=dict(size = 15, weight='bold'),
                                        title_x=0.5,
                                        xaxis_title=dict(text='Categoría', font=dict(size = 12, weight='bold')),
                                        yaxis_title=dict(text='Nº binomios', font=dict(size = 12, weight='bold')))
            st.plotly_chart(fig, use_container_width=True)
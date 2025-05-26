import streamlit as st  # type: ignore
import pandas as pd
import psycopg2 as ps  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import numpy as np
import re
from datetime import date
import os
from src.soporte_carga_dashboard import conexion_BBDD, ejecutor_querys  # type: ignore
from dotenv import load_dotenv



# dbname = "BBDD_Hipica" # base a la que nos queremos conectar
# user = "postgres"
# password = "admin"
# host = "localhost"
# port = "5432" # puerto en el que s eencuentra postgres
load_dotenv()

dbname = os.getenv("nombre_BBDD")
user = os.getenv("usuario")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

conn = conexion_BBDD(dbname, user, password, host, port)
cur = conn.cursor()

meses = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril"
}
prueba_norma = {
    '(238.2.1)': 'Baremo A con cronómetro',
    '(238.2.2)': 'Baremo A con cronómetro y desempate',
    '(274.1.5.3)': 'Dos fases, ambas con cronómetro',
    '(274.2)': 'Dos fases especial',
    '(238.1.1)': 'Baremo A sin cronómetro',
    '(274.1.5.2)': 'Dos fases, primera sin cronómetro, segunda con cronómetro',
    '(269.3.2)': 'Prueba de potencia',
    '(263)': 'Baremo C',
    '(273.3.4)': 'Prueba con dos mangas y desempate',
    '(239)': 'Baremo A juzgado como Baremo C',
    '(264)': 'Prueba de caza',
    '(273.3.3.1)': 'Prueba con dos mangas sin desempate',
    '(276.2)': 'Prueba con puntuación progresiva',
    '(238.1.2)': 'Baremo A sin cronómetro con desempate'
}

# QUERYS BUENAS
query_n_concursos = """
        SELECT COUNT(id_concurso)
        FROM concursos c;
"""

query_concursos_mes = """
        SELECT 
                EXTRACT(MONTH FROM fecha_inicio_concurso),
                COUNT(id_concurso)
        FROM concursos c
        GROUP BY EXTRACT(MONTH FROM fecha_inicio_concurso)
        ORDER BY COUNT(id_concurso) DESC;
"""
query_concursos_ambito = """
        SELECT 
                ambito_concurso,
                CONCAT((COUNT(id_concurso)) * 100 / (SELECT COUNT(id_concurso) FROM concursos c), ' ', '%')
        FROM concursos c
        GROUP BY ambito_concurso
        ORDER BY COUNT(id_concurso) DESC;
"""

query_concursos_ambito_provincia = """
        SELECT 
                ambito_concurso,
                CONCAT((COUNT(id_concurso)) * 100 / (SELECT COUNT(id_concurso) FROM concursos c), ' ', '%')
        FROM concursos c
        GROUP BY ambito_concurso
        WHERE provincia_concurso = 'Madrid'
        ORDER BY COUNT(id_concurso) DESC;
"""

query_concursos_provincia = """
        SELECT 
                provincia_concurso,
                COUNT(id_concurso)
        FROM concursos c
        GROUP BY provincia_concurso
        ORDER BY COUNT(id_concurso) DESC;
"""

query_concursos = """ 
        SELECT DISTINCT 
                nombre_concurso, 
                fecha_inicio_concurso,
                fecha_fin_concurso
        FROM concursos c ;
"""
query_duracion_concursos = """
        
        SELECT 
                ROUND(AVG(fecha_fin_concurso::date - fecha_inicio_concurso::date), 0)
        FROM concursos c; 

"""
query_pruebas = """
        
        SELECT 
                DISTINCT SUBSTRING(
                         nombre_prueba 
                         FROM POSITION('(2' IN nombre_prueba)
                         ) as tipo_prueba, 
                COUNT(id_prueba)
        FROM pruebas p
        GROUP BY tipo_prueba
        ORDER BY 2 DESC; 
"""

query_jinetes = """ 
        SELECT DISTINCT nombre_jinete
        FROM jinetes
"""
query_caballos = """
        
        SELECT 
            DISTINCT COUNT(id_caballo)
        FROM caballos; 
"""
query_jinetes_recuento = """
        
        SELECT 
            DISTINCT COUNT(id_jinete)
        FROM jinetes; 
"""


query_categorias = """
        SELECT 
            categoria_concurso,
            COUNT(id_concurso)
        FROM concursos c
        GROUP BY categoria_concurso
        ORDER BY 1 DESC;
"""
query_concursos_pruebas_concurso = """
        
        WITH pruebas_concurso AS (
                SELECT 
                        c.id_concurso,
                        COUNT(DISTINCT p.id_prueba) as n_pruebas_concurso
                FROM resultados r
                        JOIN concursos c ON r.id_concurso = c.id_concurso
                        JOIN pruebas p ON r.id_prueba = p.id_prueba
                GROUP BY c.id_concurso
        )
        SELECT 
                ROUND(AVG(n_pruebas_concurso), 0)
        FROM pruebas_concurso;

"""

lista_nombres = [tupla[0] for tupla in ejecutor_querys(cur, query_jinetes)]
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


st.set_page_config(page_title = "Dashboard_hipica",
                    page_icon="🐎",
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    menu_items={ 'Get Help': "https://github.com/Gabijc/Proyecto_ETL_Hoteles"}) 


st.sidebar.title("Navegación de páginas")
page = st.sidebar.radio(label="Selecciona una página",
                        options=["Análisis general", "Análisis de binomios"])

# Inicializamos estado
if "vista_general" not in st.session_state:
    st.session_state.vista_general = "inicio"  # por defecto muestra el inicio

if page == "Análisis general":

    with st.container():
        col1, col2, col3 = st.columns([0.15, 1, 2])
        with col1:
            # Botones para cambiar vista
            if st.button("Inicio"):
                st.session_state.vista_general = "inicio"
        with col2:
            if st.button("Concursos"):
                st.session_state.vista_general = "concursos"

    # Vista "Inicio"
    if st.session_state.vista_general == "inicio":
        st.markdown("<h1 style='text-align: center;'>Análisis de la competición hípica</h1>", unsafe_allow_html=True)

        nombres_provincias = [row[0] for row in ejecutor_querys(cur, """SELECT DISTINCT provincia_concurso FROM concursos c;""")]
        nombres_provincias = ['General'] + nombres_provincias
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                seleccion_provincia = st.selectbox('Selecciona una o más opciones:', nombres_provincias)
        if seleccion_provincia == 'General':
            # Inyectar CSS para centrar el contenido dentro de st.metric
            st.markdown("""
                <style>
                /* Contenedor general de cada métrica */
                div[data-testid="stMetric"] {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100px;
                    padding: 0.5rem;
                }

                /* Título centrado y más grande */
                div[data-testid="stMetric"] > div:first-child {
                    text-align: center;
                    font-weight: bold;
                    font-size: 2rem;  /* Tamaño del título */
                    width: 100%;
                }

                /* Valor centrado y más grande */
                div[data-testid="stMetric"] > div:nth-child(2) {
                    text-align: center;
                    font-size: 2rem;  /* Tamaño del número */
                    width: 100%;
                    justify-content: center;
                    display: flex;
                    align-items: center;
                    height: 2.5rem;
                }
                </style>
                """, unsafe_allow_html=True)
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric("Nº concursos", f"{ejecutor_querys(cur, query_n_concursos)[0][0]}", border=True)
                col2.metric("Tipos_pruebas", f"{len(ejecutor_querys(cur, query_pruebas))}", border=True)
                col3.metric("Duracion_media_concuros", f"{ejecutor_querys(cur, query_duracion_concursos)[0][0]}", border=True)
                col4.metric("Pruebas_concurso", round(ejecutor_querys(cur, query_concursos_pruebas_concurso)[0][0]), border=True)
                col5.metric("Nº jinetes", f"{ejecutor_querys(cur, query_jinetes_recuento)[0][0]}", border=True)
                col6.metric("Nº caballos", f"{ejecutor_querys(cur, query_caballos)[0][0]}", border=True)

            with st.container():
                col1, col2 = st.columns([1.5, 1.5])
                with col1:
                    df = pd.DataFrame(ejecutor_querys(cur, query_concursos_mes)).sort_values(by=0, ascending=True)
                    df[0] = df[0].apply(lambda x: meses[int(x)])
                    fig1 = px.line(df, x=0, y=1, title='Concursos por mes')
                    fig1.update_layout(
                        title_font=dict(size=20, weight='bold'),
                        title_x=0.45,
                        xaxis_title=dict(text='Fecha', font=dict(weight='bold')),
                        yaxis_title=dict(text='Valor', font=dict(weight='bold')),
                        yaxis=dict(showgrid=True, gridcolor='lightgray', showticklabels=False),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    x_data = fig1.data[0]['x']
                    y_data = fig1.data[0]['y']
                    fig1.add_trace(go.Scatter(x=x_data, y=y_data, mode='text',
                                            text=y_data, textposition="top center",
                                            showlegend=False, textfont=dict(weight='bold')))
                    st.plotly_chart(fig1, use_container_width=True)

                with col2:
                    df = pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito))
                    df[1] = df[1].str.replace('%', '').str.strip().astype(int)
                    colores = ['#4c78a8', '#54a24b']
                    fig2 = px.pie(df, values=1, names=0, title='Porcentaje de concursos por ámbito', color_discrete_sequence=colores)
                    fig2.update_traces(textinfo='percent', textfont_color='white')
                    fig2.update_layout(width=600, 
                                    height=400, 
                                    title_x=0.5, 
                                    title_font=dict(size=16, weight='bold'))
                    st.plotly_chart(fig2, use_container_width=True)

            with st.container():
                concursos_provincias = ejecutor_querys(cur, query_concursos_provincia)
                concursos = pd.DataFrame(concursos_provincias)
                concursos[2] = round((concursos[1] / concursos[1].sum()) * 100, 2)
                df_provincias = pd.DataFrame(concursos_provincias, columns=['Provincia', 'Nº concursos'])
                fig = px.bar(df_provincias, x='Provincia', y='Nº concursos', title="Concursos por provincia")
                fig.update_layout(
                            width=10,
                            height=400,
                            title_font=dict(size=15, weight='bold'),
                            title_x=0.5,
                            xaxis_title=dict(text='Provincia', font=dict(size=12, weight='bold')),
                            yaxis_title=dict(text='Nº concursos', font=dict(size=12, weight='bold')))
                st.plotly_chart(fig, use_container_width=True)


                
            with st.container():
                col1, col2 = st.columns([1.5, 1.5])
                with col1:
                    concursos_categorias = pd.DataFrame(ejecutor_querys(cur, query_categorias)).sort_values(by = 1, ascending=False)
                    fig = px.bar(concursos_categorias, x = 0, y = 1, title = "Concursos por categoria")
                    fig.update_layout(
                                        width=800, 
                                        height=500,
                                        title_font=dict(size = 15, weight='bold'),
                                        title_x=0.5,
                                        xaxis_title=dict(text='Categoría', font=dict(size = 12, weight='bold')),
                                        yaxis_title=dict(text='Nº concursos', font=dict(size = 12, weight='bold')))
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    tipos_pruebas = pd.DataFrame(ejecutor_querys(cur, query_pruebas)).head(5)
                    tipos_pruebas["prueba"] = tipos_pruebas[0].apply(lambda x: prueba_norma.get(x) + ' ' + x)
                    fig = px.bar(tipos_pruebas, x = "prueba", y = 1, title = "Pruebas")
                    fig.update_layout(
                                        width=800, 
                                        height=550,
                                        title_font=dict(size = 15, weight='bold'),
                                        title_x=0.5,
                                        xaxis_title=dict(text='Tipo_prueba', font=dict(size = 12, weight='bold')),
                                        yaxis_title=dict(text='Nº veces', font=dict(size = 12, weight='bold')))
                    st.plotly_chart(fig, use_container_width=True) 

        else:
            with st.container():
                col1, col2 = st.columns([1.5, 1.5])
                with col1:
                    graficos_provincias(seleccion_provincia, "temporal")
                with col2:
                    graficos_provincias(seleccion_provincia, "ambitos")
            st.write(graficos_provincias(seleccion_provincia, "localidades"))
            with st.container():
                col1, col2 = st.columns([0.5, 3])
                with col1:
                    seleccion_filtro = st.selectbox("Filtros",  ["Concursos por categoría", "Dinero por categoría", "Binomios por categoría"])
                with col2:
                    graficos_provincias(seleccion_provincia, "categorias", seleccion_filtro)


    # Vista "Concursos"
    elif st.session_state.vista_general == "concursos":
        st.markdown("<h1 style='text-align: center;'>Búsqueda de resultados</h1>", unsafe_allow_html=True)
        # Inicializar vista_concurso si no está en session_state
        if "vista_concurso" not in st.session_state:
            st.session_state.vista_concurso = "lista_pruebas"
        
        # Rango mínimo y máximo del slider
        fecha_inicio = date(2025, 1, 1)
        fecha_fin = date(2025, 4, 30)

        # Slider con dos fechas
        rango_fechas = st.slider(
            "Selecciona un rango de fechas",
            min_value=fecha_inicio,
            max_value=fecha_fin,
            value=(date(2025, 1, 1), date(2025, 4, 30)),
            format="DD/MM/YYYY"
        )

        st.write("Rango de fechas seleccionado:")
        st.write("Desde:", rango_fechas[0])
        st.write("Hasta:", rango_fechas[1])

        # Obtener lista de concursos disponibles
        nombres_concursos = [row[0] for row in ejecutor_querys(cur, f""" SELECT DISTINCT nombre_concurso FROM concursos WHERE fecha_inicio_concurso >= '{rango_fechas[0]}' AND fecha_fin_concurso <= '{rango_fechas[1]}';""")]
        seleccion_concurso = st.multiselect("Selecciona uno o más concursos:", nombres_concursos)

        if seleccion_concurso:
            # Obtener las pruebas del/los concurso/s seleccionados
            df = concursos_seleccionado(seleccion_concurso).rename(columns = {0: "Concurso", 1: "Pruebas", 2: "Fecha_prueba"})

            if st.session_state.vista_concurso == "lista_pruebas":
                st.write("### Pruebas disponibles")
                st.write(df)

                # Crear opciones legibles para el selectbox
                opciones_pruebas = [
                    f"{row["Pruebas"]} - {row["Fecha_prueba"]} - {row["Concurso"]}"
                    for _, row in df.iterrows()
                ]

                seleccion = st.selectbox("Selecciona una prueba:", opciones_pruebas, index=None)

                # Botón para confirmar selección
                if seleccion and st.button("Ver resultados de esta prueba"):
                    fila = df.loc[
                        df.apply(lambda r: f"{r["Pruebas"]} - {r["Fecha_prueba"]} - {r["Concurso"]}", axis=1) == seleccion
                    ].iloc[0]

                    st.session_state.prueba_seleccionada = {
                        "nombre_prueba": fila["Pruebas"],
                        "nombre_concurso": fila["Concurso"],
                        "fecha_prueba": fila["Fecha_prueba"]
                    }
                    st.session_state.vista_concurso = "resultados"

            elif st.session_state.vista_concurso == "resultados":
                prueba = st.session_state.prueba_seleccionada

                st.write(f"## Resultados de la prueba '{prueba['nombre_prueba']}' con fecha {prueba['fecha_prueba']} para el concurso '{prueba['nombre_concurso']}'")

                query_resultados = f"""
                    SELECT 
                        r.estado,
                        r.puesto,
                        j.nombre_jinete,
                        co.nombre_caballo,
                        rs.puntos_obs_r1,
                        rs.puntos_tmp_r1,
                        rs.tiempo_r1,
                        rs.puntos_obs_r2,
                        rs.puntos_tmp_r2,
                        rs.tiempo_r2,
                        rs.puntos_obs_r3,
                        rs.puntos_tmp_r3,
                        rs.tiempo_r3
                    FROM resultados r
                        JOIN pruebas p ON r.id_prueba = p.id_prueba
                        JOIN concursos c ON r.id_concurso = c.id_concurso
                        JOIN jinetes j ON r.id_jinete = j.id_jinete
                        JOIN caballos co ON r.id_caballo = co.id_caballo
                        JOIN resultados_salto rs ON r.id_resultado = rs.id_resultado
                    WHERE p.nombre_prueba = '{prueba["nombre_prueba"]}' AND p.fecha_prueba = DATE '{prueba["fecha_prueba"]}' AND c.nombre_concurso = '{prueba['nombre_concurso']}';
                """

                resultados_df = pd.DataFrame(ejecutor_querys(cur, query_resultados))

                # Mostrar tabla de resultados
                st.dataframe(resultados_df, use_container_width=True)

                # Botón para volver a lista de pruebas
                if st.button("Volver a lista de pruebas"):
                    st.session_state.vista_concurso = "lista_pruebas"
                    st.session_state.prueba_seleccionada = None



elif page == "Análisis de binomios":
    st.markdown("<h1 style='text-align: center;'>Análisis de binomios</h1>", unsafe_allow_html=True)

    # Selección del jinete (sin selección inicial por defecto)
    opciones_jinetes = ["Selecciona un jinete..."] + lista_nombres
    jinete_seleccionado = st.selectbox("Selecciona un jinete:", opciones_jinetes, key="jinete")

    if jinete_seleccionado != "Selecciona un jinete...":
        # Obtengo la lista de caballos del jinete
        caballos_jinete_df = concursos_seleccionado(jinete_seleccionado, 'jinetes')
        if not caballos_jinete_df.empty:
            lista_caballos = ["Selecciona un caballo..."] + caballos_jinete_df[0].tolist()
            caballo_seleccionado = st.selectbox("Selecciona un caballo:", lista_caballos, key="caballo")

            if caballo_seleccionado != "Selecciona un caballo...":
                # Llamo a la función pasando los nombres seleccionados
                jinete, caballo, edad_caballo, n_concursos, alturas_buenas, promedio_puntos_obs, promedio_veces_cero, binomio = info_jinete_caballo(jinete_seleccionado, caballo_seleccionado)
                df = info_jinete_caballo(jinete, caballo)[-1]
                st.write(f"Jinete seleccionado: {jinete}")
                st.write(f"Caballo seleccionado: {caballo}")
                st.markdown("""
                <style>
                /* Contenedor general de cada métrica */
                div[data-testid="stMetric"] {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100px;
                    padding: 0.5rem;
                }

                /* Título centrado y más grande */
                div[data-testid="stMetric"] > div:first-child {
                    text-align: center;
                    font-weight: bold;
                    font-size: 2rem;  /* Tamaño del título */
                    width: 100%;
                }

                /* Valor centrado y más grande */
                div[data-testid="stMetric"] > div:nth-child(2) {
                    text-align: center;
                    font-size: 2rem;  /* Tamaño del número */
                    width: 100%;
                    justify-content: center;
                    display: flex;
                    align-items: center;
                    height: 2.5rem;
                }
                </style>
                """, unsafe_allow_html=True)
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Rango edad caballo", f"{edad_caballo}", border=True)
                    col2.metric("Numero de concursos", f"{n_concursos}", border=True)
                    col3.metric("Promedio puntos obstáculos", f"{promedio_puntos_obs}", border=True)
                    col4.metric("% veces cero puntos", f"{promedio_veces_cero:.2f}%", border=True)

                st.write(f"Pruebas en las que compite el caballo: {', '.join(alturas_buenas)}")

                with st.container():
                    col1, col2 = st.columns([1.5, 1.5])
                    with col1:
                        colores = ['#4c78a8', '#54a24b']
                        estado_counts = df['estado'].value_counts().reset_index()
                        estado_counts.columns = ['estado', 'count']
                        fig = px.pie(estado_counts, values="count", names="estado", title='Porcentaje de finalización pruebas', color_discrete_sequence=colores)
                        fig.update_traces(textinfo='percent', textfont_color='white')
                        fig.update_layout(width=600, height=400, title_x=0.5, title_font=dict(size=16, weight='bold'))
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        filtered_df = df[(df['jinete'] == jinete) & (df['caballo'] == caballo)].copy()
                        filtered_df['fecha_prueba'] = pd.to_datetime(filtered_df['fecha_prueba'])

                        if not filtered_df.empty:
                            fig = px.line(
                                filtered_df,
                                x='fecha_prueba',
                                y='puesto',
                                hover_data=['prueba', 'concurso', 'estado', 'puesto'],
                                title=f'Puesto de {jinete} con {caballo} a lo largo del tiempo')
                            fig.update_layout(
                                xaxis_title='Fecha de la Prueba',
                                yaxis_title='Puesto')
                            st.plotly_chart(fig, use_container_width=True)

                st.write(df)
            else:
                st.info("Selecciona un caballo para continuar.")
        else:
            st.info(f"No se encontraron caballos para el jinete: {jinete_seleccionado}")
    else:
        st.info("Selecciona un jinete para ver sus caballos.")






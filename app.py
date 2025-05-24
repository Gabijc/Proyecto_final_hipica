import streamlit as st  # type: ignore
import pandas as pd
import psycopg2 as ps  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import numpy as np
import re

def conexion_BBDD(nombre_BBDD, usuario, contraseña, anfitrion, puerto):

    conn = ps.connect(
                    dbname = nombre_BBDD, 
                    user = usuario,
                    password = contraseña,
                    host = anfitrion,
                    port = puerto)

    return conn

dbname = "BBDD_Hipica" # base a la que nos queremos conectar
user = "postgres"
password = "admin"
host = "localhost"
port = "5432" # puerto en el que s eencuentra postgres

conn = conexion_BBDD(dbname, user, password, host, port)
cur = conn.cursor()
# COmprobamos que la conexión está creada y conectada
cur.execute("SELECT version();")
cur.fetchone() 


def ejecutor_querys(cur, query):
    cur.execute(query)
    return cur.fetchall()

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

def info_jinete_caballo(jinete_entrada, caballo_entrada):
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
                r.puesto
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
                                                                    11: 'prueba', 12: 'concurso', 13: 'estado', 14: 'fecha_prueba', 15: 'puesto'})
    # METRICAS
    n_concursos = len(binomio['concurso'].unique()) # numero de concursos en los que el caballo ha competido con el jinete seleccionado
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

    # Promedio de puntos en obstáculos por salida
    promedio_puntos_obs = round(np.mean(salidas_pista)) # promedio de puntos de obstaculos que realiza el caballo en una salida a pista 

    # Porcentaje de salidas con 0 puntos en obstáculos
    veces_cero = sum(1 for x in salidas_pista if x == 0) # numero de veces que el caballo ha hecho cero puntos en obstaculos
    promedio_veces_cero = (veces_cero / num_salidas if num_salidas > 0 else np.nan)*100
    jinete = binomio['jinete'].unique()[0]
    caballo = binomio['caballo'].unique()[0]
    edad_caballo = edad_bueno[0] if edad_bueno else "No joven"
    return jinete, caballo, edad_caballo, n_concursos, alturas_buenas, promedio_puntos_obs, promedio_veces_cero, binomio

def graficos_provincias (provincia, grafico_buscado):

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
                        COUNT(s.id_concurso),
                        SUM(r.dinero_premio)
                FROM seleccion_provincia s
                    JOIN resultados r on s.id_concurso = r.id_concurso
                GROUP BY DISTINCT localidad_concurso;
        """
        return pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito_provincia))
    
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
                        SUM(r.dinero_premio)
                FROM seleccion_provincia s
                    JOIN resultados r on s.id_concurso = r.id_concurso
                GROUP BY DISTINCT s.categoria_concurso;
        """
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

st.set_page_config(page_title = "Dashboard_hipica",
                    page_icon="🐎",
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    menu_items={ 'Get Help': "https://github.com/Gabijc/Proyecto_ETL_Hoteles"}) 

# def set_bg_color(color):
#     st.markdown(
#         f"""
#          <style>
#          .stApp {{
#              background-color: {color};
#          }}
#          </style>
#          """,
#         unsafe_allow_html=True
#     )

# Ejemplo de uso:
#set_bg_color('#E5F6E3')  # Un verde claro


st.sidebar.title("Navegación de páginas")
page = st.sidebar.radio(label="Selecciona una página",
                        options=["Análisis general", "Análisis de binomios"])

# Inicializamos estado
if "vista_general" not in st.session_state:
    st.session_state.vista_general = "inicio"  # por defecto muestra el inicio

if page == "Análisis general":
    st.title("Análisis general")

    # Botones para cambiar vista
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Inicio"):
            st.session_state.vista_general = "inicio"
    with col2:
        if st.button("Concursos"):
            st.session_state.vista_general = "concursos"

    # Vista "Inicio"
    if st.session_state.vista_general == "inicio":

        nombres_provincias = [row[0] for row in ejecutor_querys(cur, """SELECT DISTINCT provincia_concurso FROM concursos c;""")]
        nombres_provincias = ['General'] + nombres_provincias
        seleccion_provincia = st.selectbox('Selecciona una o más opciones:', nombres_provincias)
        if seleccion_provincia == 'General':
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric("Nº concursos", f"{ejecutor_querys(cur, query_n_concursos)[0][0]}", border=True)
                col2.metric("Tipos_pruebas", f"{len(ejecutor_querys(cur, query_pruebas))}", border=True)
                col3.metric("Duracion_media_concuros", f"{ejecutor_querys(cur, query_duracion_concursos)[0][0]}", border=True)
                col4.metric("Pruebas_concurso", "9", border=True)
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
                col1, col2 = st.columns([1.5, 1.5])
                with col1:
                    concursos_provincias = ejecutor_querys(cur, query_concursos_provincia)
                    concursos = pd.DataFrame(concursos_provincias)
                    concursos[2] = round((concursos[1] / concursos[1].sum()) * 100, 2)
                    df_provincias = pd.DataFrame(concursos_provincias, columns=['Provincia', 'Nº concursos'])
                    fig = px.bar(df_provincias, x='Nº concursos', y='Provincia', title="Concursos por provincia")
                    fig.update_layout(
                            width=10,
                            height=800,
                            title_font=dict(size=15, weight='bold'),
                            title_x=0.5,
                            xaxis_title=dict(text='Provincia', font=dict(size=12, weight='bold')),
                            yaxis_title=dict(text='Nº concursos', font=dict(size=12, weight='bold')))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    tipos_pruebas = pd.DataFrame(ejecutor_querys(cur, query_pruebas)).head(5)
                    tipos_pruebas["prueba"] = tipos_pruebas[0].apply(lambda x: prueba_norma.get(x) + ' ' + x)
                    fig = px.bar(tipos_pruebas, x = "prueba", y = 1, title = "Pruebas")
                    fig.update_layout(
                                    width=800, 
                                    height=400,
                                    title_font=dict(size = 15, weight='bold'),
                                    title_x=0.5,
                                    xaxis_title=dict(text='Tipo_prueba', font=dict(size = 12, weight='bold')),
                                    yaxis_title=dict(text='Nº veces', font=dict(size = 12, weight='bold')))
                    st.plotly_chart(fig, use_container_width=True)
                
                with st.container():
                    concursos_categorias = pd.DataFrame(ejecutor_querys(cur, query_categorias))
                    fig = px.bar(concursos_categorias, x = 0, y = 1, title = "Concursos por categoria")
                    fig.update_layout(
                                    width=800, 
                                    height=400,
                                    title_font=dict(size = 15, weight='bold'),
                                    title_x=0.5,
                                    xaxis_title=dict(text='Categoría', font=dict(size = 12, weight='bold')),
                                    yaxis_title=dict(text='Nº concursos', font=dict(size = 12, weight='bold')))
                    st.plotly_chart(fig, use_container_width=True)

        else:
            graficos_provincias(seleccion_provincia, "temporal")
            graficos_provincias(seleccion_provincia, "ambitos")
            st.write(graficos_provincias(seleccion_provincia, "localidades"))
            graficos_provincias(seleccion_provincia, "categorias")



    # Vista "Concursos"
    elif st.session_state.vista_general == "concursos":
        nombres_concursos = [row[0] for row in ejecutor_querys(cur, """SELECT DISTINCT nombre_concurso FROM concursos c;""")]
        seleccion_concurso = st.multiselect('Selecciona una o más opciones:',nombres_concursos)
        seleccion_inicio = st.multiselect('Selecciona una o más opciones:',
                                          list(pd.DataFrame(ejecutor_querys(cur, query_concursos))[1]))
        seleccion_fin = st.multiselect('Selecciona una o más opciones:',
                                       list(pd.DataFrame(ejecutor_querys(cur, query_concursos))[2]))
        
        if seleccion_concurso:
            df = concursos_seleccionado(seleccion_concurso)
            st.write(df) 

        # Puedes agregar filtros o análisis adicionales aquí

elif page == "Análisis de binomios":
    st.title("Análisis de binomios")

    # Selección del jinete
    jinete_seleccionado = st.selectbox("Selecciona un jinete:", lista_nombres, key="jinete")

    if jinete_seleccionado:
        # Obtengo la lista de caballos del jinete
        caballos_jinete_df = concursos_seleccionado(jinete_seleccionado, 'jinetes')
        if not caballos_jinete_df.empty:
            lista_caballos = caballos_jinete_df[0].tolist()
            caballo_seleccionado = st.selectbox("Selecciona un caballo:", lista_caballos, key="caballo")

            if caballo_seleccionado:
                # Llamo a la función pasando los nombres seleccionados
                jinete, caballo, edad_caballo, n_concursos, alturas_buenas, promedio_puntos_obs, promedio_veces_cero, binomio = info_jinete_caballo(jinete_seleccionado, caballo_seleccionado)
                df = info_jinete_caballo(jinete, caballo)[-1]

                with st.container():
                    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
                    col1.metric("Jinete", f"{jinete}", border=True)
                    col2.metric("Caballo", f"{caballo}", border=True)
                    col3.metric("Edad caballo", f"{edad_caballo}", border=True)
                    col4.metric("Numero de concursos", f"{n_concursos}", border=True)
                    col5.metric("Alturas competidas", f"{alturas_buenas}", border=True)
                    col6.metric("Promedio puntos obstaculos", f"{promedio_puntos_obs}", border=True)
                    col7.metric("% veces cero puntos", f"{promedio_veces_cero:.2f}%", border=True)
                
                with st.container():
                    col1, col2 = st.columns([1.5, 1.5])
                    with col1:
                        colores = ['#4c78a8', '#54a24b']
                        estado_counts = df['estado'].value_counts().reset_index()
                        estado_counts.columns = ['estado', 'count']
                        fig = px.pie(estado_counts, values="count", names="estado", title='Porcentaje de finalización pruebas', color_discrete_sequence=colores)
                        fig.update_traces(textinfo='percent', textfont_color='white')
                        fig.update_layout(width=600, height=400, title_x=0.5, title_font=dict(size = 16, weight='bold'))
                        st.plotly_chart(fig, use_container_width=True)
                    with col2: 

                        filtered_df = df[(df['jinete'] == jinete) & (df['caballo'] == caballo)].copy()

                        # Ensure 'fecha_prueba' is in datetime format
                        filtered_df['fecha_prueba'] = pd.to_datetime(filtered_df['fecha_prueba'])

                        if not filtered_df.empty:
                            fig = px.line(
                                filtered_df,
                                x='fecha_prueba',
                                y='puesto',
                                hover_data=['prueba', 'concurso', 'estado', 'puesto'],
                                title=f'Puesto de {jinete} con {caballo} Over Time')
                            fig.update_layout(
                                xaxis_title='Fecha de la Prueba',
                                yaxis_title='Puesto')
                            st.plotly_chart(fig, use_container_width=True)

                # Aquí puedes añadir más análisis o gráficos con la variable 'binomio' (DataFrame)
                st.write(df) 
            else:
                st.info("Selecciona un caballo para continuar.")
        else:
            st.info(f"No se encontraron caballos para el jinete: {jinete_seleccionado}")
    else:
        st.info("Selecciona un jinete para ver sus caballos.")





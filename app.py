import streamlit as st  # type: ignore
import pandas as pd
import psycopg2 as ps  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore

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
def concursos_seleccionado(elementos, coso = 'info_concursos'):
    
    if coso == "info_concursos":
        if not elementos:
                return pd.DataFrame()
        concursos_str = ', '.join([f"'{c}'" for c in elementos])
        query = f""" 
                SELECT *
                FROM resultados r
                JOIN pruebas p ON r.id_prueba = p.id_prueba
                JOIN concursos c ON r.id_concurso = c.id_concurso
                WHERE c.nombre_concurso IN ({concursos_str});
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
                        options=["Análisis general", "Análisis de binomios", "Acceso a resultados"])

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
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Nº concursos", f"{ejecutor_querys(cur, query_n_concursos)[0][0]}", border=True)
            col2.metric("Tipos_pruebas", f"{len(ejecutor_querys(cur, query_pruebas))}", border=True)
            col3.metric("Duracion_media_concuros", f"{ejecutor_querys(cur, query_duracion_concursos)[0][0]}", border=True)
            col4.metric("Pruebas_concurso", "9", border=True)

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
                fig = px.bar(df_provincias, x='Provincia', y='Nº concursos', title="Concursos por provincia")
                fig.update_layout(
                        width=800,
                        height=400,
                        title_font=dict(size=15, weight='bold'),
                        title_x=0.5,
                        xaxis_title=dict(text='Provincia', font=dict(size=12, weight='bold')),
                        yaxis_title=dict(text='Nº concursos', font=dict(size=12, weight='bold')))
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                tipos_pruebas = pd.DataFrame(ejecutor_querys(cur, query_pruebas))
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

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            nombres_jinetes = ["hugo álvarez amaro", "otro jinete", "etc."]
            jinete_seleccionado_col1 = st.selectbox("Selecciona un jinete:", nombres_jinetes, key="jinete_col1")

            if jinete_seleccionado_col1:
                caballos_jinete_df = concursos_seleccionado(jinete_seleccionado_col1, 'jinetes')
                if not caballos_jinete_df.empty:
                    lista_caballos = caballos_jinete_df[0].tolist()
                    caballos_seleccionados_col1 = st.multiselect("Caballos del jinete:", lista_caballos, key="caballos_col1")
                    if caballos_seleccionados_col1:
                        st.write("Caballos seleccionados:", caballos_seleccionados_col1)
                    else:
                        st.info("Selecciona al menos un caballo.")
                else:
                    st.info(f"No se encontraron caballos para el jinete: {jinete_seleccionado_col1}")
            else:
                st.info("Selecciona un jinete para ver sus caballos.")

        with col2:
            nombres_jinetes = ["hugo álvarez amaro", "otro jinete", "etc."]
            jinete_seleccionado_col2 = st.selectbox("Selecciona un jinete:", nombres_jinetes, key="jinete_col2")

            if jinete_seleccionado_col2:
                caballos_jinete_df = concursos_seleccionado(jinete_seleccionado_col2, 'jinetes')
                if not caballos_jinete_df.empty:
                    lista_caballos = caballos_jinete_df[0].tolist()
                    caballos_seleccionados_col2 = st.multiselect("Caballos del jinete:", lista_caballos, key="caballos_col2")
                    if caballos_seleccionados_col2:
                        st.write("Caballos seleccionados:", caballos_seleccionados_col2)
                    else:
                        st.info("Selecciona al menos un caballo.")
                else:
                    st.info(f"No se encontraron caballos para el jinete: {jinete_seleccionado_col2}")
            else:
                st.info("Selecciona un jinete para ver sus caballos.")



elif page == "Acceso a resultados":
    st.title("Acceso a resultados")

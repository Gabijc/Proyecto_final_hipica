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
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
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
query_duracion_concursos = """
        
        SELECT 
                ROUND(AVG(fecha_fin_concurso::date - fecha_inicio_concurso::date), 0)
        FROM concursos c; 

"""

query_concursos_provincia = """
        SELECT 
                provincia_concurso,
                COUNT(id_concurso)
        FROM concursos c
        GROUP BY provincia_concurso
        ORDER BY COUNT(id_concurso) DESC;
"""


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
page = st.sidebar.radio(label = "Selecciona una página",
                        options = ["Análisis general", "Análisis de binomios", "Acceso a resultados"])

if page == "Análisis general":
    st.title("Análisis general")
    with st.container():
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Nº concursos", f"{ejecutor_querys(cur, query_n_concursos)[0][0]}",  border = True)
            col2.metric("Tipos_pruebas", f"{len(ejecutor_querys(cur, query_pruebas))}",  border = True)
            col3.metric("Duracion_media_concuros", f"{ejecutor_querys(cur, query_duracion_concursos)[0][0]}", border = True)
            col4.metric("Pruebas_concurso", "9", border = True)


    with st.container():
        col1, col2 = st.columns([1.5, 1.5])
        with col1:

            df = pd.DataFrame(ejecutor_querys(cur, query_concursos_mes)).sort_values(by=0, ascending=True)
            df[0] = df[0].apply(lambda x: meses[int(x)])

            fig1 = px.line(df, x=0, y=1, title='Concursos por mes')
            fig1.update_layout(
                title_font=dict(size = 20, weight='bold'),
                title_x=0.45,
                xaxis_title=dict(text='Fecha', font=dict(weight='bold')),
                yaxis_title=dict(text='Valor', font=dict(weight='bold')),
                plot_bgcolor='white',
                yaxis=dict(showgrid=True, gridcolor='lightgray', showticklabels=False),
                # xaxis=dict(showline=True, tickfont=dict(weight='bold')),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            x_data = fig1.data[0]['x']
            y_data = fig1.data[0]['y']

            # Añade una nueva traza con los números
            fig1.add_trace(go.Scatter(x=x_data, y=y_data,
                                    mode='text',
                                    text=y_data,
                                    textposition="top center",
                                    showlegend=False,
                                    textfont=dict(weight='bold')))
            st.plotly_chart(fig1, use_container_width = True) # mostramos el gráfico

        with col2:
            df = pd.DataFrame(ejecutor_querys(cur, query_concursos_ambito))
            # Convert percentage strings to integers
            df[1] = df[1].str.replace('%', '').str.strip().astype(int)
            colores = ['#4c78a8', '#54a24b']
            fig2 = px.pie(df, values=1, names=0, title='Porcentaje de concursos por ámbito', color_discrete_sequence=colores)
            fig2.update_traces(textinfo='percent', textfont_color='white')
            fig2.update_layout(width=600, height=400, title_x=0.5, title_font=dict(size = 16, weight='bold'))
            st.plotly_chart(fig2, use_container_width = True) # mostramos el gráfico

    with st.container():
        col1, col2 = st.columns([1.5, 1.5])
        with col1:
            concursos_provincias = ejecutor_querys(cur, query_concursos_provincia)
            concursos = pd.DataFrame(concursos_provincias)
            concursos[2] = round((concursos[1]/concursos[1].sum())*100, 2)
        
            df_provincias = pd.DataFrame(concursos_provincias, columns=['Provincia', 'Nº concursos'])

            fig = px.bar(df_provincias, x='Provincia', y='Nº concursos', title = "Concursos por provincia")
            fig.update_layout(
                width=800, 
                height=400,
                title_font=dict(size = 15, weight='bold'),
                title_x=0.5,
                xaxis_title=dict(text='Provincia', font=dict(size = 12, weight='bold')),
                yaxis_title=dict(text='Nº concursos', font=dict(size = 12, weight='bold')),
                plot_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width = True) # mostramos el gráfico

elif page == "Análisis de binomios":
    st.title("Análisis de binomios")
    

elif page == "Acceso a resultados":
    st.title("Acceso a resultados")
    # Aquí puedes agregar el código para acceder a los resultados
    pass
import streamlit as st  # type: ignore


st.set_page_config(page_title = "Dashboard_hipica",
                    page_icon="🐎",
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    menu_items={ 'Get Help': "https://github.com/Gabijc/Proyecto_ETL_Hoteles"}) 

def set_bg_color(color):
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-color: {color};
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

# Ejemplo de uso:
#set_bg_color('#E5F6E3')  # Un verde claro


st.sidebar.title("Navegación de páginas")
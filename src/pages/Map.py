import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from datetime import time, datetime
import numpy as np


st.set_page_config(page_title="Mapa de Criminalidad", page_icon="./assets/Logo-removebg.png")

@st.cache_data
def load_data():
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "Dataset", "test.csv")
    
    try:
        df = pd.read_csv(csv_path)
        
        required_cols = ["X", "Y", "PdDistrict", "DayOfWeek", "Dates", "Address"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"El CSV debe contener estas columnas: {required_cols}")
            st.stop()
            
        
        df["X"] = pd.to_numeric(df["X"], errors='coerce')
        df["Y"] = pd.to_numeric(df["Y"], errors='coerce')
        df = df.dropna(subset=["X", "Y"])
        
        
        df["Dates"] = pd.to_datetime(df["Dates"])
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        st.error(f"Ruta intentada: {csv_path}")
        st.stop()


df = load_data()


st.title("🚨 Mapa de Criminalidad")
st.markdown("Visualización interactiva de incidentes")


st.sidebar.header("Filtros")
distritos = st.sidebar.multiselect(
    "Distritos",
    options=df["PdDistrict"].unique(),
    default=df["PdDistrict"].unique()
)

dias = st.sidebar.multiselect(
    "Días de semana",
    options=df["DayOfWeek"].unique(),
    default=df["DayOfWeek"].unique()
)


hora_min, hora_max = st.sidebar.slider(
    "Rango horario",
    min_value=time(0, 0),
    max_value=time(23, 59),
    value=(time(0, 0), time(23, 59))
)


df_filtrado = df[
    (df["PdDistrict"].isin(distritos)) &
    (df["DayOfWeek"].isin(dias))
]


df_filtrado["Hour"] = df_filtrado["Dates"].dt.time
df_filtrado = df_filtrado[
    (df_filtrado["Hour"] >= hora_min) &
    (df_filtrado["Hour"] <= hora_max)
]


data_for_deck = df_filtrado[["X", "Y", "PdDistrict", "Address", "Dates"]].to_dict('records')


layer = pdk.Layer(
    "ScatterplotLayer",
    data=data_for_deck,
    get_position=["X", "Y"],
    get_color=[255, 0, 0, 160],
    get_radius=100,
    pickable=True,
    auto_highlight=True
)


view_state = pdk.ViewState(
    latitude=df_filtrado["Y"].mean(),
    longitude=df_filtrado["X"].mean(),
    zoom=11,
    pitch=50
)


tooltip = {
    "html": "<b>Distrito:</b> {PdDistrict}<br><b>Dirección:</b> {Address}<br><b>Fecha:</b> {Dates}",
    "style": {"background": "steelblue", "color": "white"}
}


try:
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    )
    st.pydeck_chart(deck)
except Exception as e:
    st.error(f"Error al mostrar el mapa: {str(e)}")


st.subheader("📊 Estadísticas")
col1, col2, col3 = st.columns(3)
col1.metric("Total incidentes", len(df_filtrado))
col2.metric("Distritos", len(distritos))
col3.metric("Días analizados", len(dias))


st.dataframe(df_filtrado[["Dates", "DayOfWeek", "PdDistrict", "Address"]])
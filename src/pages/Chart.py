import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="DataFrame Demo", page_icon="./assets/Logo-removebg.png")

st.markdown("# Índice de Criminalidad")

st.subheader("Selecciona un distrito")


@st.cache_data
def get_crime_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "Dataset", "test.csv")

    if not os.path.exists(csv_path):
        st.error("El archivo de datos no se encuentra en la ruta esperada.")
        return None

    df = pd.read_csv(csv_path)
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

try:
    df = get_crime_data()

    if df is not None:

        district_options = list(df["PdDistrict"].unique())
        selected_district = st.selectbox("Elige un distrito:", district_options)

        st.sidebar.header("Selecciona el tipo de gráfico")
        graph_option = st.sidebar.radio(
            "Elige una vista:",
            ["Tendencia Temporal (Área)", "Dispersión vs. Fecha", "Comparación por Distrito (Barras)"]
        )

        df_filtered = df[df["PdDistrict"] == selected_district]

        st.markdown(f"## Criminalidad en {selected_district}")

        if graph_option == "Tendencia Temporal (Área)":
            df_area = df_filtered.groupby(df_filtered["Dates"].dt.date).size().reset_index(name="Cantidad de Delitos")

            chart_area = (
                alt.Chart(df_area)
                .mark_area(opacity=0.3)
                .encode(
                    x="Dates:T",
                    y="Cantidad de Delitos:Q"
                )
            )
            st.altair_chart(chart_area, use_container_width=True)

        elif graph_option == "Dispersión vs. Fecha":
            df_scatter = df_filtered.groupby(df_filtered["Dates"].dt.date).size().reset_index(
                name="Cantidad de Delitos")

            scatter_chart = (
                alt.Chart(df_scatter)
                .mark_circle(size=60)
                .encode(
                    x="Dates:T",
                    y="Cantidad de Delitos:Q"
                )
            )

            regression_chart = alt.Chart(df_scatter).transform_regression(
                "Dates", "Cantidad de Delitos"
            ).mark_line(color="red").encode(
                x="Dates:T",
                y="Cantidad de Delitos:Q"
            ).properties(title="Regresión Lineal")

            st.altair_chart(scatter_chart + regression_chart, use_container_width=True)

            if df_scatter.dropna().shape[0] > 1:
                correlation = df_scatter.dropna().corr().iloc[0, 1]
                st.markdown(f"**Coeficiente de correlación entre Fecha y Número de Delitos:** `{correlation:.2f}`")
            else:
                st.markdown("**No hay suficientes datos para calcular la correlación.**")

        elif graph_option == "Comparación por Distrito (Barras)":
            df_bars = df.groupby("PdDistrict").size().reset_index(name="Cantidad de Delitos")

            bar_chart = (
                alt.Chart(df_bars)
                .mark_bar()
                .encode(
                    x="PdDistrict:N",
                    y="Cantidad de Delitos:Q",
                    color="PdDistrict:N"
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)

        st.write("### Datos detallados del distrito seleccionado")
        st.dataframe(df_filtered)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

st.markdown(
    """
        <hr style="margin-top: 50px;"/>
        <div style="text-align: center; color: gray;">
            <small>By Miguel Rojas</small>
        </div>
        """,
    unsafe_allow_html=True
)

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
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )

import streamlit as st
import pandas as pd
import altair as alt
from config.db import conn

st.set_page_config(page_title="Crime Index", page_icon="./assets/Logo-removebg.png")

st.markdown("# 🧭 Crime Index")
st.subheader("Select a district")

@st.cache_data
def get_crime_data():
    try:
        pipeline = [
            {
                "$project": {
                    "PdDistrict": 1,
                    "Dates": 1
                }
            },
            {"$limit": 10000}  
        ]
        docs = list(conn.aggregate(pipeline))
        df = pd.DataFrame(docs)

        if df.empty:
            return None

        df["Dates"] = pd.to_datetime(df["Dates"], errors='coerce')
        df = df.dropna(subset=["Dates", "PdDistrict"])
        return df

    except Exception as e:
        st.error(f"Error loading data from MongoDB: {str(e)}")
        return None

try:
    df = get_crime_data()

    if df is not None:
        district_options = sorted(df["PdDistrict"].dropna().unique())
        selected_district = st.selectbox("Choose a district:", district_options)

        st.sidebar.header("Select chart type")
        graph_option = st.sidebar.radio(
            "Choose a view:",
            ["Time Trend (Area)", "Scatter vs. Date", "District Comparison (Bars)"]
        )

        df_filtered = df[df["PdDistrict"] == selected_district]

        st.markdown(f"## Crime in {selected_district}")

        if graph_option == "Time Trend (Area)":
            df_area = df_filtered.groupby(df_filtered["Dates"].dt.date).size().reset_index(name="Crime Count")

            chart_area = (
                alt.Chart(df_area)
                .mark_area(opacity=0.3)
                .encode(
                    x="Dates:T",
                    y="Crime Count:Q"
                )
            )
            st.altair_chart(chart_area, use_container_width=True)

        elif graph_option == "Scatter vs. Date":
            df_scatter = df_filtered.groupby(df_filtered["Dates"].dt.date).size().reset_index(
                name="Crime Count"
            )

            scatter_chart = (
                alt.Chart(df_scatter)
                .mark_circle(size=60)
                .encode(
                    x="Dates:T",
                    y="Crime Count:Q"
                )
            )

            regression_chart = alt.Chart(df_scatter).transform_regression(
                "Dates", "Crime Count"
            ).mark_line(color="red").encode(
                x="Dates:T",
                y="Crime Count:Q"
            ).properties(title="Linear Regression")

            st.altair_chart(scatter_chart + regression_chart, use_container_width=True)

            if df_scatter.dropna().shape[0] > 1:
                correlation = df_scatter.dropna().corr().iloc[0, 1]
                st.markdown(f"**Correlation coefficient between Date and Crime Count:** `{correlation:.2f}`")
            else:
                st.markdown("**Not enough data to calculate correlation.**")

        elif graph_option == "District Comparison (Bars)":
            df_bars = df.groupby("PdDistrict").size().reset_index(name="Crime Count")

            bar_chart = (
                alt.Chart(df_bars)
                .mark_bar()
                .encode(
                    x="PdDistrict:N",
                    y="Crime Count:Q",
                    color="PdDistrict:N"
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)

        st.write("### Detailed data for selected district")
        st.dataframe(df_filtered.head(50))

except Exception as e:
    st.error(f"Error loading data: {e}")

st.markdown(
    """
        <hr style="margin-top: 50px;"/>
        <div style="text-align: center; color: gray;">
            <small>By Miguel Rojas</small>
        </div>
        """,
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.api.types import CategoricalDtype
from pages_functions.zone_comp_funcs import get_crime_data
from Machine.ComparatorZoneReport import generate_comparative_analysis


st.set_page_config(
    page_title="Zone Comparator",
    page_icon="./assets/Logo-removebg.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333333;
    }
    h1, h2, h3, h4 {
        color: #0a3d62;
        font-weight: 700;
    }
    .stMetric {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .element-container > div > div > div > div > div {
        border-radius: 15px !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
    }
    button[kind="primary"] {
        background-color: #0a3d62 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Zone Comparator")
st.write("""
Easily compare two areas of San Francisco based on their crime levels. 
Visualize the most frequent crime types, explore comparative charts, and if available, check citizen perception data.
Ideal for understanding safety differences between neighborhoods quickly, visually, and informatively.
""")


df = get_crime_data()

if df.empty:
    st.error("No crime data found. Please check the database connection.")
    st.stop()


df["Dates"] = pd.to_datetime(df["Dates"], errors='coerce')
df = df.dropna(subset=['Dates'])
df["Hour"] = df["Dates"].dt.hour
df["DayOfWeek"] = df["Dates"].dt.day_name()

zones = sorted(df["PdDistrict"].dropna().unique())
col1, col2 = st.columns(2)
with col1:
    zone1 = st.selectbox("Select Zone 1", zones)
with col2:
    zone2 = st.selectbox("Select Zone 2", zones, index=1 if zones[0] == zone1 else 0)

df_zone1 = df[df["PdDistrict"] == zone1].copy()
df_zone2 = df[df["PdDistrict"] == zone2].copy()

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
cat_type = CategoricalDtype(categories=days_order, ordered=True)
df_zone1["DayOfWeek"] = df_zone1["DayOfWeek"].astype(cat_type)
df_zone2["DayOfWeek"] = df_zone2["DayOfWeek"].astype(cat_type)


st.subheader("Total crime level")
col1, col2 = st.columns(2)
with col1:
    st.metric(f"Crimes in {zone1}", len(df_zone1))
with col2:
    st.metric(f"Crimes in {zone2}", len(df_zone2))

bar_data = pd.DataFrame({
    "Zone": [zone1, zone2],
    "Total Crimes": [len(df_zone1), len(df_zone2)]
})
fig_bar = px.bar(bar_data, x="Zone", y="Total Crimes", color="Zone", title="Crime comparison by zone")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")


st.subheader("Zone ranking by crime")
ranking = df["PdDistrict"].value_counts().reset_index()
ranking.columns = ["Zone", "Total Crimes"]
st.dataframe(ranking, use_container_width=True)

st.markdown("---")


st.subheader("🕵️‍♂️ Most frequent crime types (Top 10)")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{zone1}**")
    top_zone1 = df_zone1["Category"].value_counts().head(10)
    fig1 = px.bar(top_zone1, x=top_zone1.values, y=top_zone1.index, orientation='h',
                  labels={'x': 'Count', 'index': 'Crime'}, title=f"Top crimes in {zone1}")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.markdown(f"**{zone2}**")
    top_zone2 = df_zone2["Category"].value_counts().head(10)
    fig2 = px.bar(top_zone2, x=top_zone2.values, y=top_zone2.index, orientation='h',
                  labels={'x': 'Count', 'index': 'Crime'}, title=f"Top crimes in {zone2}")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")


st.subheader("Crime type proportion")
col1, col2 = st.columns(2)
with col1:
    pie1 = px.pie(
        df_zone1["Category"].value_counts().head(5),
        values=df_zone1["Category"].value_counts().head(5).values,
        names=df_zone1["Category"].value_counts().head(5).index,
        title=f"Top 5 crimes in {zone1}"
    )
    st.plotly_chart(pie1, use_container_width=True)
with col2:
    pie2 = px.pie(
        df_zone2["Category"].value_counts().head(5),
        values=df_zone2["Category"].value_counts().head(5).values,
        names=df_zone2["Category"].value_counts().head(5).index,
        title=f"Top 5 crimes in {zone2}"
    )
    st.plotly_chart(pie2, use_container_width=True)

st.markdown("---")


st.subheader("Crime map by zone")
col1, col2 = st.columns(2)
with col1:
    if 'X' in df_zone1.columns and 'Y' in df_zone1.columns:
        fig_map1 = px.scatter_mapbox(
            df_zone1, lat="Y", lon="X", hover_name="Category",
            color="Category", zoom=12, height=300,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig_map1, use_container_width=True)
    else:
        st.info("No coordinates available for this zone.")
with col2:
    if 'X' in df_zone2.columns and 'Y' in df_zone2.columns:
        fig_map2 = px.scatter_mapbox(
            df_zone2, lat="Y", lon="X", hover_name="Category",
            color="Category", zoom=12, height=300,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig_map2, use_container_width=True)
    else:
        st.info("No coordinates available for this zone.")

st.markdown("---")


st.subheader("Hourly crime distribution")
hour_zone1 = df_zone1["Hour"].value_counts().sort_index()
hour_zone2 = df_zone2["Hour"].value_counts().sort_index()
hour_df = pd.DataFrame({
    "Hour": range(24),
    zone1: hour_zone1.reindex(range(24), fill_value=0),
    zone2: hour_zone2.reindex(range(24), fill_value=0)
})
fig_hour = px.line(hour_df, x="Hour", y=[zone1, zone2], markers=True,
                   labels={"value": "Crime Count", "variable": "Zone"},
                   title="Crimes by hour of day")
st.plotly_chart(fig_hour, use_container_width=True)

st.markdown("---")


st.subheader("Comparison question")

user_question = st.text_input("Ask about patterns, differences or risks between the two zones:")

if user_question:
    with st.spinner("Analyzing..."):
        response = generate_comparative_analysis(df_zone1, df_zone2, zone1, zone2, user_question)
        st.text_area("Analysis", value=response, height=300)

st.markdown("---")


st.subheader("Filtered data download")
col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label=f"Download {zone1} data",
        data=df_zone1.to_csv(index=False),
        file_name=f"crime_{zone1}.csv",
        mime="text/csv"
    )
with col2:
    st.download_button(
        label=f"Download {zone2} data",
        data=df_zone2.to_csv(index=False),
        file_name=f"crime_{zone2}.csv",
        mime="text/csv"
    )

st.markdown("---")
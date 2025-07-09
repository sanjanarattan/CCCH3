import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.title("Exploratory Data Analysis: People Receiving Homeless Response Services in Contra Costa County (2017–2024)")

conn = sqlite3.connect("ccc_homelessness.db")

query_disabled = "SELECT CALENDAR_YEAR, PERSONSWITHDISABILITY FROM disabled"
df_disabled = pd.read_sql_query(query_disabled, conn)
df_disabled["PERSONSWITHDISABILITY"] = pd.to_numeric(df_disabled["PERSONSWITHDISABILITY"], errors="coerce")
df_disabled = df_disabled.dropna()
df_disabled["Error_Disabled"] = df_disabled["PERSONSWITHDISABILITY"] * 0.05

query_veteran = "SELECT CALENDAR_YEAR, VETERANCOUNTS FROM veteran"
df_veteran = pd.read_sql_query(query_veteran, conn)
df_veteran["VETERANCOUNTS"] = pd.to_numeric(df_veteran["VETERANCOUNTS"], errors="coerce")
df_veteran = df_veteran.dropna()
df_veteran["Error_Veteran"] = df_veteran["VETERANCOUNTS"] * 0.05

df_merged = pd.merge(df_disabled, df_veteran, on="CALENDAR_YEAR", how="outer").sort_values("CALENDAR_YEAR")

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=df_merged["CALENDAR_YEAR"],
    y=df_merged["PERSONSWITHDISABILITY"],
    mode='lines+markers',
    name='Disabled',
    error_y=dict(type='data', array=df_merged["Error_Disabled"], visible=True)
))

fig1.add_trace(go.Scatter(
    x=df_merged["CALENDAR_YEAR"],
    y=df_merged["VETERANCOUNTS"],
    mode='lines+markers',
    name='Veteran',
    error_y=dict(type='data', array=df_merged["Error_Veteran"], visible=True)
))

fig1.update_layout(
    title="Persons Receiving Services by Disabled/ Veteran Status",
    xaxis_title="Year",
    yaxis_title="Number of Persons",
    legend_title="Group"
)

st.plotly_chart(fig1)

st.write("Disabled population data show consistent growth that appears to accelerate over time. Veteran population trends remains relatively stable.")


query_age = "SELECT CALENDAR_YEAR, AGE_GROUP_PUBLIC, EXPERIENCING_HOMELESSNESS_CNT FROM age"
df_age = pd.read_sql_query(query_age, conn)
df_age["EXPERIENCING_HOMELESSNESS_CNT"] = pd.to_numeric(df_age["EXPERIENCING_HOMELESSNESS_CNT"], errors="coerce")
df_age = df_age.dropna()

fig2 = px.line(
    df_age,
    x="CALENDAR_YEAR",
    y="EXPERIENCING_HOMELESSNESS_CNT",
    color="AGE_GROUP_PUBLIC",
    title="Persons Receiving Services by Age Over Time",
    labels={"CALENDAR_YEAR": "Year", "EXPERIENCING_HOMELESSNESS_CNT": "Number of Persons", "AGE_GROUP_PUBLIC": "Age Group"}
)

st.plotly_chart(fig2)

st.write("Youth services (Under 18) have increased dramatically from ~1,100 in 2017 to ~1,800 in 2024 (63% increase), although this group is the biggest group. Total service recipients have increased substantially, with most age groups showing upward trends after 2021-2022. There's a notable dip across most age groups around 2020-2021, likely reflecting pandemic-related service disruptions, followed by recovery and growth.")

query_race = """
SELECT CALENDAR_YEAR, RACE_ETHNICITY, CNT 
FROM race 
WHERE ALONE_OR_IN_COMBINATION = 'Alone'
""" 
df_race = pd.read_sql_query(query_race, conn)
df_race["CNT"] = pd.to_numeric(df_race["CNT"], errors="coerce")
df_race["CALENDAR_YEAR"] = df_race["CALENDAR_YEAR"].astype(str)

df_race = df_race.dropna()


fig3 = px.bar(
    df_race,
    x="CALENDAR_YEAR",
    y="CNT",
    color="RACE_ETHNICITY",
    title="Persons Receiving Services by Race/Ethnicity",
    labels={"CALENDAR_YEAR": "Year", "CNT": "Count"},
)

fig3.update_layout(barmode='stack', xaxis_title="Year", yaxis_title="Count")

st.plotly_chart(fig3)


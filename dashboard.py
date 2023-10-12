import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

# Load cleaned data
all_df = pd.read_csv("./dashboard/main_data.csv")

#all_df.sort_values(by="datetime", inplace=True)
all_df.reset_index(inplace=True)

#for column in datetime_columns:
all_df["datetime"] = pd.to_datetime(all_df["datetime"])

# Filter data
min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    st.sidebar.header("Please Filter Here")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
station = st.sidebar.selectbox(
    "Select the Station:",
    options=all_df["station"].unique()
)

main_df = all_df[(all_df["datetime"] >= str(start_date)) & 
                (all_df["datetime"] <= str(end_date))]

column_df1 = main_df[["datetime", "station", "kesehatan", "AQI"]].sort_values(by="AQI").head(5)

st.header('Dicoding Air Quality Index (AQI) Dashboard :sparkles:')
st.header('General Info')

st.subheader("Monthly AQI Average in All Chinese Station")
monthly_AQI_df = all_df.resample(rule='M', on='datetime').agg({
    "AQI": "mean"
})
monthly_AQI_df.index = monthly_AQI_df.index.strftime('%B, %Y')
monthly_AQI_df = monthly_AQI_df.reset_index()
monthly_AQI_df.rename(columns={
    "AQI": "AQI mean",
}, inplace=True)
fig, ax = plt.subplots(figsize=(25, 8))
ax.plot(
    monthly_AQI_df["datetime"],
    monthly_AQI_df["AQI mean"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation= 45)

st.pyplot(fig)

st.subheader("Pollutants Avg Concentration in Period of Time")
 
fig, ax = plt.subplots(nrows=1, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

pollutantsdata_df = main_df[["PM2.5", "PM10", "SO2", "NO2", "O3"]].melt()
test123_df = pollutantsdata_df.groupby(by="variable").agg({
    "value" : "mean"
})
 
sns.barplot(x="value", y="variable", data=test123_df, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel("concentration", fontsize=30)
ax.set_title("Mean Polutants data", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

# Station performance
st.subheader("Best & Worst Chinese Station by Avg in Period of Time")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

bestworst_station_df = main_df[["station", "AQI"]].groupby(by="station").agg({
    "AQI": "mean",
})

sns.barplot(x="AQI", y="station", data=bestworst_station_df.sort_values(by="AQI", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("AQI mean", fontsize=30)
ax[0].set_title("Best Station by AQI", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="AQI", y="station", data=bestworst_station_df.sort_values(by="AQI", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("AQI mean", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Station by AQI", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)



st.header('GeoAnalysis Info by Station: ' + "".join(station))

specificstation_df = main_df.query(
    "station == @station"
)

st.subheader("Monthly AQI Average in: " + "".join(station) + " station")
monthlyspecific_AQI_df = specificstation_df.resample(rule='M', on='datetime').agg({
    "AQI": "mean"
})
monthlyspecific_AQI_df.index = monthlyspecific_AQI_df.index.strftime('%B, %Y')
monthlyspecific_AQI_df = monthlyspecific_AQI_df.reset_index()
monthlyspecific_AQI_df.rename(columns={
    "AQI": "AQI mean",
}, inplace=True)
fig, ax = plt.subplots(figsize=(25, 8))
ax.plot(
    monthlyspecific_AQI_df["datetime"],
    monthlyspecific_AQI_df["AQI mean"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation= 45)

st.pyplot(fig)

st.subheader("Pollutants Avg Concentration in Period of Time " + "".join(station) + " station")
 
fig, ax = plt.subplots(nrows=1, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

pollutantsdata_df = specificstation_df[["PM2.5", "PM10", "SO2", "NO2", "O3"]].melt()
test123_df = pollutantsdata_df.groupby(by="variable").agg({
    "value" : "mean"
})
 
sns.barplot(x="value", y="variable", data=test123_df, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel("concentration", fontsize=30)
ax.set_title("Mean Polutants data", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)


st.subheader("Pollutants Influence to AQI (Air Quality Index) " + "".join(station) + " station")

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(35, 25))
sns.scatterplot(data=specificstation_df, x="AQI", y="PM2.5", hue="kesehatan", style="kesehatan", ax=ax[0,0]) 
ax[0,0].set_title("PM2.5 concentration vs AQI", loc="center", fontsize=20)
ax[0,0].tick_params(axis='y', labelsize=20)
ax[0,0].tick_params(axis='x', labelsize=15, rotation= 45)

sns.scatterplot(data=specificstation_df, x="AQI", y="PM10", hue="kesehatan", style="kesehatan", ax=ax[0,1]) 
ax[0,1].set_title("PM10 concentration vs AQI", loc="center", fontsize=20)
ax[0,1].tick_params(axis='y', labelsize=20)
ax[0,1].tick_params(axis='x', labelsize=15, rotation= 45)

sns.scatterplot(data=specificstation_df, x="AQI", y="SO2", hue="kesehatan", style="kesehatan", ax=ax[0,2]) 
ax[0,2].set_title("SO2 concentration vs AQI", loc="center", fontsize=20)
ax[0,2].tick_params(axis='y', labelsize=20)
ax[0,2].tick_params(axis='x', labelsize=15, rotation= 45)

sns.scatterplot(data=specificstation_df, x="AQI", y="NO2", hue="kesehatan", style="kesehatan", ax=ax[1,0]) 
ax[1,0].set_title("NO2 concentration vs AQI", loc="center", fontsize=20)
ax[1,0].tick_params(axis='y', labelsize=20)
ax[1,0].tick_params(axis='x', labelsize=15, rotation= 45)

sns.scatterplot(data=specificstation_df, x="AQI", y="CO", hue="kesehatan", style="kesehatan", ax=ax[1,1]) 
ax[1,1].set_title("CO concentration vs AQI", loc="center", fontsize=20)
ax[1,1].tick_params(axis='y', labelsize=20)
ax[1,1].tick_params(axis='x', labelsize=15, rotation= 45)

sns.scatterplot(data=specificstation_df, x="AQI", y="O3", hue="kesehatan", style="kesehatan", ax=ax[1,2]) 
ax[1,2].set_title("O3 concentration vs AQI", loc="center", fontsize=20)
ax[1,2].tick_params(axis='y', labelsize=20)
ax[1,2].tick_params(axis='x', labelsize=15, rotation= 45)


st.pyplot(fig)




st.caption('Copyright © SubmisiDicoding 2023')
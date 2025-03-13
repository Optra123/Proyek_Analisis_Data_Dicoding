import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_pollution_trend_pivot(df):
    pollution_trend_pivot = df.pivot_table(
        values=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'],
        index=['station', 'year'],
        aggfunc='mean'
    )
    pollution_trend_pivot['total_pollution'] = pollution_trend_pivot.sum(axis=1)
    pollution_trend_pivot = pollution_trend_pivot.reset_index()
    return pollution_trend_pivot

def create_pm25_pivot(df):
    pm25_pivot = df.pivot_table(
        values='PM2.5',
        index='year',
        columns='station',
        aggfunc='mean'
    ).sort_values(by=[2013, 2014, 2015, 2016, 2017], ascending=False, axis=1)
    return pm25_pivot

def create_correlation_pivot(df):
    correlation_pivot = df.groupby(['station', 'year'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
    return correlation_pivot

all_data = pd.read_csv('https://raw.githubusercontent.com/Optra123/Proyek_Analisis_Data_Dicoding/refs/heads/main/dashboard/data.csv')
pollution_trend = create_pollution_trend_pivot(all_data)
pm25_by_station = create_pm25_pivot(all_data)
correlation_matrix = create_correlation_pivot(all_data)


st.title('Analisis Kualitas Udara di Beijing')

# Sidebar
st.sidebar.title('Pengaturan')
selected_station = st.sidebar.selectbox('Pilih Stasiun', pollution_trend['station'].unique())
selected_year = st.sidebar.slider('Pilih Tahun', 2013, 2017, 2013)

# Filter data berdasarkan pilihan di sidebar
filtered_pollution_trend = pollution_trend[
    (pollution_trend['station'] == selected_station) & (pollution_trend['year'] == selected_year)
]
filtered_pm25_by_station = pm25_by_station.loc[[selected_year]]
filtered_correlation_matrix = correlation_matrix.loc[(selected_station, selected_year)]


# Menampilkan grafik tren polusi
st.header('Tren Polusi')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='year', y='total_pollution', data=pollution_trend[pollution_trend['station'] == selected_station], ax=ax)
ax.set_title(f'Tren Polusi di Stasiun {selected_station}')
ax.set_xlabel('Tahun')
ax.set_ylabel('Total Polusi')
st.pyplot(fig)


# Menampilkan bar chart PM2.5 tertinggi
st.header('Rata-rata PM2.5 Tertinggi')
fig, ax = plt.subplots(figsize=(10, 6))
plt.bar(pm25_by_station.columns, pm25_by_station.loc[selected_year])
plt.title(f'Rata-rata PM2.5 Tertinggi di Setiap Stasiun - Tahun {selected_year}')
plt.xlabel('Stasiun')
plt.ylabel('Rata-rata PM2.5')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

# Menampilkan heatmap korelasi
st.header('Korelasi antara PM2.5 dan Polutan Lainnya')
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(filtered_correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax, yticklabels=filtered_correlation_matrix.index)  
plt.title(f'Korelasi Polutan dengan PM2.5 di Stasiun {selected_station} - Tahun {selected_year}')
st.pyplot(fig)
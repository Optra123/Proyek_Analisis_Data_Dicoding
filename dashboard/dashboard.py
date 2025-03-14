import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membuat pivot table rata-rata
def create_yearly_avg_pollution(df):
    yearly_avg_pollution = df.groupby('year')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()
    yearly_avg_pollution['total_pollution'] = yearly_avg_pollution.sum(axis=1)
    return yearly_avg_pollution

def create_station_avg_pm25(df):
    station_avg_pm25 = df.groupby('station')['PM2.5'].mean().reset_index()
    station_avg_pm25 = station_avg_pm25.rename(columns={'PM2.5': 'average_pm25'}) 
    station_avg_pm25 = station_avg_pm25.set_index('station').T 
    return station_avg_pm25

def create_correlations(df):
    correlations = df.groupby(['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().corr()
    return correlations 



# Membaca data
all_data = pd.read_csv('https://raw.githubusercontent.com/Optra123/Proyek_Analisis_Data_Dicoding/refs/heads/main/dashboard/data.csv')

# Membuat pivot table
pollution_trend = create_yearly_avg_pollution(all_data)
pm25_by_station = create_station_avg_pm25(all_data)
correlation_matrix = create_correlations(all_data)


st.set_page_config(page_title="Analisis Kualitas Udara di Beijing", page_icon=":bar_chart:", layout="wide")
st.title('Analisis Kualitas Udara di Beijing')
st.markdown("---") 


tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3"])

# Tab 1: Tren Polusi
with tab1:
    st.header('Tren Polusi')
    st.write("Grafik ini menunjukkan tren rata-rata total polusi di semua stasiun selama periode 2013-2017.")
    fig, ax = plt.subplots(figsize=(8, 4)) 
    sns.lineplot(x='year', y='total_pollution', data=pollution_trend, ax=ax)
    ax.set_title('Tren Polusi di Semua Stasiun')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Total Polusi')
    ax.set_xticks(pollution_trend.index)  
    st.pyplot(fig)

# Tab 2: Rata-rata PM2.5 Tertinggi
with tab2:
    st.header('Rata-rata PM2.5 Tertinggi')
    st.write("Grafik ini menunjukkan rata-rata PM2.5 tertinggi di setiap stasiun untuk setiap tahun.")
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.bar(pm25_by_station.columns, pm25_by_station.loc['average_pm25'])  
    plt.title(f'Rata-rata PM2.5 Tertinggi di Setiap Stasiun')
    plt.xlabel('Stasiun')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

# Tab 3: Korelasi antara PM2.5 dan Polutan Lainnya
with tab3:
    st.header('Korelasi antara PM2.5 dan Polutan Lainnya')
    st.write("Heatmap ini menunjukkan korelasi rata-rata antar polutan.")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Korelasi Rata-rata Antar Polutan')
    st.pyplot(fig)
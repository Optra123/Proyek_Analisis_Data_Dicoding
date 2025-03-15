import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul dan deskripsi
st.title("Dashboard Polusi Udara di Beijing 📊")  
st.markdown("Dashboard ini menampilkan analisis polusi udara di Beijing berdasarkan data dari 12 stasiun pengukuran selama tahun 2013 - 2017.")

# Sidebar filters
st.sidebar.header("Filter Data 🔍")
selected_station = st.sidebar.selectbox("Pilih Stasiun", pd.unique(pd.read_csv('https://raw.githubusercontent.com/Optra123/Proyek_Analisis_Data_Dicoding/refs/heads/main/dashboard/all_data.csv')['station']))
selected_year = st.sidebar.selectbox("Pilih Tahun", pd.unique(pd.read_csv('https://raw.githubusercontent.com/Optra123/Proyek_Analisis_Data_Dicoding/refs/heads/main/dashboard/all_data.csv')['year']))

# Membaca data
df = pd.read_csv('https://raw.githubusercontent.com/Optra123/Proyek_Analisis_Data_Dicoding/refs/heads/main/dashboard/all_data.csv')
filtered_df = df[(df['station'] == selected_station) & (df['year'] == selected_year)]

# Visualisasi 1: Tren Polusi
st.header("Tren Polusi Udara 📈")
st.markdown("Grafik ini menunjukkan tren perubahan total polusi udara per bulan.")
monthly_avg = filtered_df.groupby('month')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().sum(axis=1)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_avg.index, monthly_avg.values)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Polusi")
ax.set_title(f"Tren Polusi di Stasiun {selected_station} - Tahun {selected_year}")
st.pyplot(fig)

# Visualisasi 2: Rata-rata PM2.5
st.header("Rata-rata PM2.5 Bulanan 🌫️")
st.markdown("Grafik ini menunjukkan rata-rata PM2.5 per bulan.")
monthly_pm25 = filtered_df.groupby('month')['PM2.5'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(monthly_pm25.index, monthly_pm25.values)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title(f"Rata-rata PM2.5 di Stasiun {selected_station} - Tahun {selected_year}")
st.pyplot(fig)

# Visualisasi 3: Korelasi Polutan
st.header("Korelasi Antar Polutan 🌡️")
st.markdown("Heatmap ini menunjukkan korelasi antara PM2.5 dan polutan lainnya.")
corr_matrix = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title(f"Korelasi Polutan di Stasiun {selected_station} - Tahun {selected_year}")
st.pyplot(fig)
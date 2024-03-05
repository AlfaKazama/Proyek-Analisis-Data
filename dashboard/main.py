import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_weathersit_df(df):
    weathersit_df = df.groupby('weathersit')['cnt'].sum().reset_index()
    return weathersit_df

def create_workingday_df(df):    
    # Mengelompokkan data berdasarkan working day
    workingday_df = df.groupby('workingday').agg({
    'cnt':['sum'],
    'registered':['sum'],
    'casual':['sum']
    
    })
    return workingday_df

# Load cleaned data
day_df = pd.read_csv("day.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/AlfaKazama/Proyek-Analisis-Data/raw/main/raw/sepeda.jpg")
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

# Mengonversi objek tanggal menjadi datetime
start_date, end_date = pd.to_datetime(date_range)

main_df = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]

# Menyiapkan berbagai dataframe
weathersit_df = create_weathersit_df(main_df)
workingday_df = create_workingday_df(main_df)

# Plot tren berdasarkan kondisi cuaca
st.subheader('Peminjaman Sepeda Berdasarkan Kondisi Cuaca')

# Menambahkan boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(x='weathersit', y='cnt', data=main_df, palette='Set2')
plt.title('Peminjaman Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Peminjaman')
plt.xticks(ticks=[0, 1, 2], labels=['Clear', 'Cloudy', 'Rain'])
st.pyplot(plt.gcf())

# Menampilkan Boxplot
st.subheader('Perbedaan Jumlah Pengguna Sepeda antara Hari Kerja dan Hari Libur')

# Membuat plot boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(x='workingday', y='cnt', data=main_df, palette='Set1')
plt.title('Perbedaan Jumlah Pengguna Sepeda antara Hari Kerja dan Hari Libur')
plt.ylabel('Jumlah Sepeda (cnt)')
plt.xlabel('Hari')
plt.xticks(ticks=[0, 1], labels=['Working Days', 'Holiday'])  # Mengubah label sumbu x
st.pyplot(plt.gcf())

# Membuat PLot pengguna saat weekend & holiday Vs working day berdasarkan tipe pengguna
st.subheader('Pengguna Weekend & Holiday VS Working Day Berdasar tipe Pengguna')
# Memilih data dari DataFrame
casual_data = workingday_df['casual']['sum']
registered_data = workingday_df['registered']['sum']
index = ['Weekend and Holiday', 'Working Day']

# Mengatur lebar bar
bar_width = 0.35

# Menyiapkan posisi bar
bar_positions1 = range(len(casual_data))
bar_positions2 = [pos + bar_width for pos in bar_positions1]

# Membuat bar plot
fig, ax = plt.subplots()
ax.bar(bar_positions1, casual_data, width=bar_width, label='Casual', alpha=0.7)
ax.bar(bar_positions2, registered_data, width=bar_width, label='Registered', alpha=0.7)

# Menambahkan angka pengguna pada bar
for i, data in enumerate(casual_data):
    ax.text(i, data + 100, str(data), ha='center', va='bottom', fontsize=10)

for i, data in enumerate(registered_data):
    ax.text(i + bar_width, data + 100, str(data), ha='center', va='bottom', fontsize=10)

# Menandai sumbu dan judul
ax.set_xlabel('Day Type')
ax.set_ylabel('Total Users')
ax.set_title('Total Users by Day Type')

# Menandai sumbu x
ax.set_xticks([pos + bar_width/2 for pos in bar_positions1])
ax.set_xticklabels(index)

# Menambahkan legenda
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)

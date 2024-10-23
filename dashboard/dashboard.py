import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Set up layout untuk dashboard - harus di atas sebagai perintah pertama
st.set_page_config(page_title="PM2.5 Air Quality Dashboard", layout="wide")

# Load dataset
@st.cache
def load_data():
    df = pd.read_csv('dashboard/PRSA_Data_Aotizhongxin_20130301-20170228.csv')  # Sesuaikan path dataset
    return df

df_final = load_data()

# Judul dan deskripsi
st.title("PM2.5 Air Quality Analysis Dashboard")
st.write("""
Dashboard ini menganalisis kualitas udara berdasarkan konsentrasi PM2.5 dan melihat hubungan antara suhu dan arah angin terhadap tingkat polusi udara.
""")

# Sidebar untuk memilih analisis
st.sidebar.header("Pilih Analisis")
analysis_type = st.sidebar.selectbox("Pilih Analisis", 
                                     ("Dampak Suhu terhadap PM2.5", "Pengaruh Arah Angin terhadap Polusi"))

# Fungsi Kategorisasi PM2.5
def categorize_pm25(value):
    if value <= 50:
        return 'Baik'
    elif value <= 100:
        return 'Sedang'
    elif value <= 150:
        return 'Buruk'
    elif value <= 200:
        return 'Sangat Buruk'
    else:
        return 'Berbahaya'

# Tambahkan kolom kategori berdasarkan PM2.5
df_final['Kategori PM2.5'] = df_final['PM2.5'].apply(categorize_pm25)

# --- Analisis Pertama: Dampak Suhu terhadap PM2.5 ---
if analysis_type == "Dampak Suhu terhadap PM2.5":
    
    st.header("Dampak Suhu terhadap PM2.5")
    
    # Scatter plot PM2.5 vs Suhu
    st.subheader("Scatter Plot PM2.5 vs Suhu")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='TEMP', y='PM2.5', data=df_final, s=10)
    plt.title('Hubungan antara Suhu dan PM2.5')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    st.pyplot(plt.gcf())  # Render plot
    
    # Regresi Linier antara Suhu dan PM2.5
    st.subheader("Regresi Linier Suhu vs PM2.5")
    X = df_final['TEMP']
    y = df_final['PM2.5']
    X = sm.add_constant(X)  # Tambahkan konstanta untuk regresi
    model = sm.OLS(y, X).fit()
    st.write(model.summary())

# --- Analisis Kedua: Pengaruh Arah Angin terhadap Polusi ---
elif analysis_type == "Pengaruh Arah Angin terhadap Polusi":
    
    st.header("Pengaruh Arah Angin terhadap Polusi")
    
    # Box plot PM2.5 berdasarkan arah angin
    st.subheader("Box Plot PM2.5 Berdasarkan Arah Angin")
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='wd', y='PM2.5', data=df_final)
    plt.title('Distribusi PM2.5 Berdasarkan Arah Angin')
    plt.xlabel('Arah Angin')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    st.pyplot(plt.gcf())
    
    # Bar plot rata-rata PM2.5 berdasarkan arah angin
    st.subheader("Rata-rata PM2.5 Berdasarkan Arah Angin")
    mean_pm25_by_wd = df_final.groupby('wd')['PM2.5'].mean().reset_index()
    mean_pm25_by_wd.columns = ['Arah Angin', 'Rata-rata PM2.5 (µg/m³)']
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Arah Angin', y='Rata-rata PM2.5 (µg/m³)', data=mean_pm25_by_wd, color='skyblue')
    plt.title('Rata-rata PM2.5 Berdasarkan Arah Angin')
    plt.xlabel('Arah Angin')
    plt.ylabel('Rata-rata PM2.5 (µg/m³)')
    st.pyplot(plt.gcf())

# --- Kesimpulan ---
st.sidebar.header("Kesimpulan")
if st.sidebar.checkbox("Tampilkan Kesimpulan"):
    st.subheader("Kesimpulan Analisis")
    st.write("""
    1. **Dampak Suhu terhadap PM2.5:**
       Suhu memiliki hubungan yang sangat lemah terhadap konsentrasi PM2.5. Meskipun hubungan ini signifikan secara statistik, faktor-faktor lain kemungkinan memiliki pengaruh yang lebih besar terhadap polusi udara.

    2. **Pengaruh Arah Angin terhadap Polusi:**
       Arah angin dari timur (E dan ENE) cenderung membawa polusi lebih tinggi, sedangkan arah angin dari utara dan barat laut cenderung membawa udara yang lebih bersih.
    """)

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.write("**Dashboard oleh [Nama Anda]**")

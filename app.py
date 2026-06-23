import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# KONFIGURASI HALAMAN
# =====================
st.set_page_config(
    page_title="Dashboard Nur Huda",
    page_icon="📊",
    layout="wide"
)

# =====================
# HEADER
# =====================
st.markdown(
    """
    <h1 style='text-align:center;color:#1E88E5;'>
    👨‍💻 NUR HUDA
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align:center;color:gray;'>
    Dashboard Analisis Data Pelanggan
    </h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================
# LOAD DATA (AMAN)
# =====================
@st.cache_data
def load_data():

    separators = [";", ",", "\t"]

    for sep in separators:

        try:

            df = pd.read_csv(
                "data_pelanggan.csv",
                sep=sep,
                encoding="utf-8"
            )

            # Jika kolom terbaca lebih dari 1 berarti berhasil
            if len(df.columns) > 1:
                return df

        except:
            continue

    return None


df = load_data()

# Jika gagal membaca file
if df is None:

    st.error("❌ File data_pelanggan.csv tidak dapat dibaca")

    st.info("""
    Pastikan:
    - Nama file adalah data_pelanggan.csv
    - File berada satu folder dengan app.py
    - Format file CSV benar
    """)

    st.stop()

# =====================
# TAMPILKAN KOLOM
# =====================
st.subheader("📋 Preview Data")

st.dataframe(df.head())

st.write("Jumlah baris:", len(df))
st.write("Jumlah kolom:", len(df.columns))

st.write("Nama kolom:")

st.write(list(df.columns))

st.divider()

# =====================
# KPI OTOMATIS
# =====================

angka = df.select_dtypes(include="number")

if len(angka.columns) > 0:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Data",
            len(df)
        )

    with col2:

        st.metric(
            "Jumlah Kolom",
            len(df.columns)
        )

    with col3:

        st.metric(
            "Rata-rata",
            round(
                angka.iloc[:,0].mean(),
                2
            )
        )

# =====================
# GRAFIK OTOMATIS
# =====================

kategori = df.select_dtypes(include="object")

if len(kategori.columns) > 0:

    st.subheader("📊 Grafik Distribusi")

    kolom = kategori.columns[0]

    data = df[kolom].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        data,
        labels=data.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

# =====================
# DOWNLOAD
# =====================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Data CSV",
    data=csv,
    file_name="data_pelanggan_download.csv",
    mime="text/csv",
    key="download_csv"
)

# =====================
# FOOTER
# =====================

st.divider()

st.markdown(
    """
    <center>
    © 2026 | Dibuat oleh <b>Nur Huda</b>
    </center>
    """,
    unsafe_allow_html=True
)

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
    <h1 style='text-align:center; color:#1E88E5;'>
    👨‍💻 NUR HUDA
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align:center; color:gray;'>
    Dashboard Analisis Data Pelanggan
    </h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    return pd.read_csv("data_pelanggan.csv")

df = load_data()

# =====================
# FILTER SIDEBAR
# =====================
st.sidebar.title("🔍 Filter Data")

gender = st.sidebar.multiselect(
    "Jenis Kelamin",
    df["Jenis Kelamin"].unique(),
    default=df["Jenis Kelamin"].unique()
)

profesi = st.sidebar.multiselect(
    "Profesi",
    df["Profesi"].unique(),
    default=df["Profesi"].unique()
)

filtered_df = df[
    (df["Jenis Kelamin"].isin(gender)) &
    (df["Profesi"].isin(profesi))
]

# =====================
# KPI
# =====================
st.subheader("📈 Ringkasan Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Pelanggan",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Rata-rata Umur",
        round(filtered_df["Umur"].mean(), 1)
    )

with col3:
    st.metric(
        "Total Nilai Belanja",
        f"Rp {filtered_df['Nilai Belanja Setahun'].sum():,.0f}"
    )

st.divider()

# =====================
# GRAFIK
# =====================
col1, col2 = st.columns(2)

# Pie Chart Jenis Kelamin
with col1:

    st.subheader("Distribusi Jenis Kelamin")

    gender_count = filtered_df["Jenis Kelamin"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        gender_count,
        labels=gender_count.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)


# Bar Chart Profesi
with col2:

    st.subheader("Jumlah Pelanggan per Profesi")

    profesi_count = filtered_df["Profesi"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        profesi_count.index,
        profesi_count.values
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

st.divider()

# =====================
# TABEL DATA
# =====================
st.subheader("📋 Data Pelanggan")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================
# DOWNLOAD CSV
# =====================
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Data CSV",
    data=csv,
    file_name="data_pelanggan_filter.csv",
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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Data Pelanggan",
    layout="wide"
)

# Judul
st.title("📊 Dashboard Data Pelanggan")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data_pelanggan.csv", sep=";")
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("Filter Data")

gender = st.sidebar.multiselect(
    "Jenis Kelamin",
    options=df["Jenis Kelamin"].unique(),
    default=df["Jenis Kelamin"].unique()
)

profesi = st.sidebar.multiselect(
    "Profesi",
    options=df["Profesi"].unique(),
    default=df["Profesi"].unique()
)

# Filter dataframe
filtered_df = df[
    (df["Jenis Kelamin"].isin(gender)) &
    (df["Profesi"].isin(profesi))
]

# KPI
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

# Grafik 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Jenis Kelamin")

    gender_count = filtered_df["Jenis Kelamin"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        gender_count,
        labels=gender_count.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig)

with col2:
    st.subheader("Jumlah Pelanggan per Profesi")

    profesi_count = filtered_df["Profesi"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        profesi_count.index,
        profesi_count.values
    )

    ax.set_ylabel("Jumlah")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# Grafik 2
st.subheader("Total Belanja Berdasarkan Tipe Residen")

belanja_residen = filtered_df.groupby(
    "Tipe Residen"
)["Nilai Belanja Setahun"].sum()

fig, ax = plt.subplots()

ax.bar(
    belanja_residen.index,
    belanja_residen.values
)

ax.set_ylabel("Nilai Belanja")

st.pyplot(fig)

# Tabel data
st.subheader("Data Pelanggan")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Data CSV",
    data=csv,
    file_name="data_pelanggan_filter.csv",
    mime="text/csv"
)

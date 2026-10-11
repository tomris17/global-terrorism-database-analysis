import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Global Terrorism Database Analysis",
    page_icon="🌍",
    layout="wide",
)


@st.cache_data
def load_data():
  df = pd.read_csv("terrorism_cleaned.csv")
  return df


df = load_data()

st.title("🌍 Global Terrorism Database Analysis (1970 - 2017)")
st.write(
    "Bu uygulama, küresel terörizm veritabanını kullanarak yıllara göre"
    " saldırı trendlerini, coğrafi dağılımları ve etkilenen bölgeleri analiz"
    " eder."
)

# Sidebar Filtreleri
st.sidebar.header("Filtreleme Paneli")
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Yıl Aralığı Seçin", min_year, max_year, (2000, 2017)
)

regions = ["Tümü"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Bölge Seçin", regions)

# Veriyi filtreleme
filtered_df = df[
    (df["Year"] >= selected_years[0]) & (df["Year"] <= selected_years[1])
]
if selected_region != "Tümü":
  filtered_df = filtered_df[filtered_df["Region"] == selected_region]

st.subheader(f"Filtrelenen Veri Kapsamında Olay Sayısı: {len(filtered_df):,}")

# 1. Yıllara Göre Olay Sayısı Trendi
st.markdown("### 📊 Yıllara Göre Terör Olayları Trendi")
yearly_counts = filtered_df["Year"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(
    x=yearly_counts.index,
    y=yearly_counts.values,
    ax=ax,
    color="#d9534f",
    linewidth=2.5,
    marker="o",
)
ax.set_xlabel("Yıl", fontsize=12)
ax.set_ylabel("Olay Sayısı", fontsize=12)
st.pyplot(fig)

# 2. Bölgelere veya Ülkelere Göre Dağılım
col1, col2 = st.columns(2)

with col1:
  st.markdown("### 🗺️ En Çok Olay Görülen İlk 10 Ülke")
  top_countries = filtered_df["Country"].value_counts().head(10)
  fig, ax = plt.subplots(figsize=(8, 5))
  sns.barplot(
      x=top_countries.values, y=top_countries.index, ax=ax, palette="rocket"
  )
  ax.set_xlabel("Olay Sayısı")
  ax.set_ylabe  l("Ülke")
  st.pyplot(fig)

with col2:
  st.markdown("### ⚔️ En Sık Kullanılan Saldırı Türleri")
  top_attacks = filtered_df["AttackType"].value_counts().head(10)
  fig, ax = plt.subplots(figsize=(8, 5))
  sns.barplot(
      x=top_attacks.values, y=top_attacks.index, ax=ax, palette="viridis"
  )
  ax.set_xlabel("Olay Sayısı")
  ax.set_ylabel("Saldırı Türü")
  st.pyplot(fig)

# 3. Harita / Coğrafi Dağılım (Koordinatlar üzerinden)
if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
  st.markdown("### 📍 Olayların Coğrafi Konum Dağılımı (Harita)")
  map_data = filtered_df[["latitude", "longitude"]].dropna()
  if not map_data.empty:
    st.map(map_data.rename(columns={"latitude": "lat", "longitude": "lon"}))
import streamlit as st
import pandas as pd

# =====================================================
# LOAD DATASET
# =====================================================

DATASET_PATH = "./dataset/dataset_OCR_preprocessing.csv"

df = pd.read_csv(DATASET_PATH)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Dashboard Informasi Kependudukan",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("Dashboard Informasi Kependudukan")

st.write(f"Total Data: {len(df)}")

# =====================================================
# SEARCH BY NAME ONLY
# =====================================================

search_query = st.text_input(
    "Search Nama"
)

# =====================================================
# FILTER PEKERJAAN
# =====================================================

pekerjaan_options = sorted(
    df["Pekerjaan"]
    .dropna()
    .unique()
    .tolist()
)

selected_pekerjaan = st.selectbox(
    "Pekerjaan",
    ["Semua"] + pekerjaan_options
)

# =====================================================
# FILTER AGAMA
# =====================================================

agama_options = sorted(
    df["Agama"]
    .dropna()
    .unique()
    .tolist()
)

selected_agama = st.selectbox(
    "Agama",
    ["Semua"] + agama_options
)

# =====================================================
# FILTER JENIS Kelamin
# =====================================================

jenis_kelamin_options = sorted(
    df["Jenis Kelamin"]
    .dropna()
    .unique()
    .tolist()
)

selected_jenis_kelamin = st.selectbox(
    "Jenis Kelamin",
    ["Semua"] + jenis_kelamin_options
)

# =====================================================
# FILTER USIA
# =====================================================

min_usia = int(df["Usia"].min())

max_usia = int(df["Usia"].max())

usia_range = st.slider(
    "Range Usia",
    min_usia,
    max_usia,
    (min_usia, max_usia)
)

# =====================================================
# FILTERING
# =====================================================

filtered_df = df.copy()

# =====================================================
# SEARCH FILTER (NAMA ONLY)
# =====================================================

if search_query:

    filtered_df = filtered_df[
        filtered_df["Nama"]
        .astype(str)
        .str.contains(
            search_query,
            case=False,
            na=False
        )
    ]

# =====================================================
# FILTER PEKERJAAN
# =====================================================

if selected_pekerjaan != "Semua":

    filtered_df = filtered_df[
        filtered_df["Pekerjaan"] == selected_pekerjaan
    ]

# =====================================================
# FILTER AGAMA
# =====================================================

if selected_agama != "Semua":

    filtered_df = filtered_df[
        filtered_df["Agama"] == selected_agama
    ]

# =====================================================
# FILTER AGAMA
# =====================================================

if selected_jenis_kelamin != "Semua":

    filtered_df = filtered_df[
        filtered_df["Jenis Kelamin"] == selected_jenis_kelamin
    ]


# =====================================================
# FILTER USIA
# =====================================================

filtered_df = filtered_df[
    (filtered_df["Usia"] >= usia_range[0])
    &
    (filtered_df["Usia"] <= usia_range[1])
]

# =====================================================
# ONLY SHOW SAFE COLUMNS
# =====================================================

display_columns = [

    "Nama",

    "Jenis Kelamin",

    "Kecamatan",

    "Agama",

    "Pekerjaan",

    "Usia"
]

filtered_df = filtered_df[display_columns]

# =====================================================
# RESULT
# =====================================================

st.write(f"Jumlah Result: {len(filtered_df)}")

st.dataframe(
    filtered_df,
    use_container_width=True
)

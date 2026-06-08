import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Dashboard Informasi Kependudukan",
    layout="wide"
)

# =====================================================
# LOAD DATASET
# =====================================================

DATASET_PATH = DATASET_PATH = "./dataset/dataset_OCR_preprocessing.csv"

@st.cache_data
def load_data(path):

    df = pd.read_csv(
        path,
        dtype={"NIK": str}
    )

    return df

df = load_data(DATASET_PATH)

# =====================================================
# TITLE
# =====================================================

st.title("Dashboard Informasi Kependudukan")

# =====================================================
# OVERVIEW
# =====================================================

st.header("Overview Data")


with st.expander("Lihat Seluruh Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

# =====================================================
# QUERY SECTION
# =====================================================

st.header("Filter dan Query Data")

# =====================================================
# PILIH KOLOM
# =====================================================

selected_columns = st.multiselect(
    "Pilih Kolom",
    options=df.columns.tolist(),
    default=[
        "Nama",
        "Jenis Kelamin",
        "Kecamatan",
        "Agama",
        "Pekerjaan",
        "Usia"
    ]
)

# =====================================================
# FILTER DINAMIS
# =====================================================

st.subheader("Filter")

selected_filters = {}

for column in selected_columns:

    # ==========================================
    # NUMERIC
    # ==========================================

    if pd.api.types.is_numeric_dtype(df[column]):

        min_value = float(df[column].min())

        max_value = float(df[column].max())

        selected_filters[column] = st.slider(
            f"{column}",
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
            key=f"slider_{column}"
        )

    # ==========================================
    # TEXT / CATEGORY
    # ==========================================

    else:

        options = sorted(
            df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_filters[column] = st.multiselect(
            f"{column}",
            options=options,
            default=[],
            key=f"filter_{column}"
        )

# =====================================================
# BUTTON
# =====================================================

run_query = st.button(
    "Tampilkan Hasil",
    type="primary"
)

# =====================================================
# PROCESS QUERY
# =====================================================

if run_query:

    filtered_df = df.copy()

    for column, value in selected_filters.items():

        # ======================================
        # NUMERIC FILTER
        # ======================================

        if pd.api.types.is_numeric_dtype(df[column]):

            filtered_df = filtered_df[
                (filtered_df[column] >= value[0])
                &
                (filtered_df[column] <= value[1])
            ]

        # ======================================
        # CATEGORY FILTER
        # ======================================

        else:

            if len(value) > 0:

                filtered_df = filtered_df[
                    filtered_df[column]
                    .astype(str)
                    .isin(value)
                ]

    # ==========================================
    # OUTPUT KOLOM YANG DICENTANG
    # ==========================================

    if len(selected_columns) > 0:

        filtered_df = filtered_df[
            selected_columns
        ]

    st.header("Hasil Query")

    st.success(
        f"Jumlah Data Ditemukan: {len(filtered_df)}"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Hasil Query",
        csv,
        "hasil_query.csv",
        "text/csv"
    )

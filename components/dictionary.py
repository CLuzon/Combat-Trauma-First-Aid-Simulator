import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def load_dictionary():
    file_path = Path(__file__).parent.parent / "db/dictionary.xlsx"

    return pd.read_excel(
        file_path,
        usecols = ["name", "explanation"]
    )
    

@st.dialog("辞書", width=800)
def show_dictionary():
    dictionary_df = load_dictionary()
    st.subheader("戦闘外傷救護：辞書")

    st.dataframe(
        dictionary_df,
        use_container_width=True,
        hide_index=True,
    )

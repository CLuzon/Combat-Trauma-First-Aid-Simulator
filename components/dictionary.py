import streamlit as st
import pandas as pd
from pathlib import Path
from components.field_manual_theme import apply_field_manual_theme
from components.ui_loader import render_html


@st.cache_data
def load_dictionary():
    file_path = Path(__file__).parent.parent / "db/dictionary.xlsx"
    return pd.read_excel(file_path, usecols=["name", "explanation"])


@st.dialog("用語索引", width=900)
def show_dictionary():
    apply_field_manual_theme()
    dictionary_df = load_dictionary()

    render_html("dictionary.html")

    keyword = st.text_input(
        "索引語を検索",
        placeholder="例：止血、気道、搬送",
    )

    filtered_df = dictionary_df
    if keyword:
        mask = (
            dictionary_df["name"].astype(str).str.contains(keyword, case=False, na=False)
            | dictionary_df["explanation"]
            .astype(str)
            .str.contains(keyword, case=False, na=False)
        )
        filtered_df = dictionary_df.loc[mask]

    st.caption(f"INDEX ENTRIES：{len(filtered_df)} / {len(dictionary_df)}")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "name": st.column_config.TextColumn("用語", width="medium"),
            "explanation": st.column_config.TextColumn("説明", width="large"),
        },
    )

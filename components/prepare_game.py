import streamlit as st
import pandas as pd
from components.field_manual_theme import apply_field_manual_theme
from components.ui_loader import render_html

tp_df = pd.read_excel("db/stories.xlsx", sheet_name="topic")

if "filter_id" not in st.session_state:
    st.session_state.filter_id = None
if "take_switch" not in st.session_state:
    st.session_state.take_switch = False




@st.dialog("シナリオ索引")
def show_filter():
    apply_field_manual_theme()
    parent_tp = tp_df.loc[tp_df["parent_value"] == -1, ["id_tp", "tag"]]

    st.markdown(
        '<div class="manual-code">SCENARIO INDEX / SELECT TRAINING RECORD</div>',
        unsafe_allow_html=True,
    )

    with st.container(height=360, border=True, horizontal_alignment="center"):
        for number, row in enumerate(parent_tp.itertuples(index=False), start=1):
            if st.button(f"{number:02d}　{row.tag}", width=440):
                st.session_state.filter_id = row.id_tp
                st.session_state.take_switch = True
                st.rerun()


st.set_page_config(
    page_title="モード選択",
    page_icon="▤",
    layout="centered",
)
apply_field_manual_theme()

render_html(
    "home.html",
    {
        "title": "訓練モードを選択T",
        "document_code": "FIELD MEDICAL TRAINING MANUAL / MODULE SELECT",
        "description": "無作為にシナリオを開始するか、索引から特定の訓練記録を指定すること。",
        "classification": "TRAINING MODE"
    }
)


with st.container(width="stretch", horizontal_alignment="center"):
    if st.button("01　ノーマル訓練", width=260):
        st.session_state.filter_id = None
        st.session_state.take_switch = True

    if st.button("02　シナリオ索引", width=260):
        show_filter()

    if st.button("03　前頁へ戻る", width=260):
        st.switch_page("components/home.py")

st.markdown(
    '<div class="manual-note">SELECT ONE TRAINING PROCEDURE</div>',
    unsafe_allow_html=True,
)

if st.session_state.take_switch:
    st.session_state.take_switch = False
    st.switch_page("components/game.py")

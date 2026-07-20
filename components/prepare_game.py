import streamlit as st
import pandas as pd

tp_df = pd.read_excel("db/stories.xlsx", sheet_name="topic")

if "filter_id" not in st.session_state:
    st.session_state.filter_id = None
if "take_switch" not in st.session_state:
    st.session_state.take_switch = False

@st.dialog("シナリオ選択")
def show_filter():
    parent_tp = tp_df.loc[tp_df["parent_value"] == -1, ["id_tp", "tag"]]

    with st.container(height=300, border=True, horizontal_alignment="center"):
        for row in parent_tp.itertuples(index=False):
            if st.button(row.tag, width=400):
                st.session_state.filter_id =  row.id_tp
                st.session_state.take_switch = True
                st.rerun()


st.set_page_config(
    page_title="モード選択",
    layout="centered"
)

st.header(
    "ゲームモードを選択",
    text_alignment="center"
)

with st.container(
    width="stretch",
    horizontal_alignment="center"
):
    if st.button("ノーマル", width=200):
        st.session_state.filter_id = None
        st.session_state.take_switch = True

    if st.button("シナリオ選択", width=200):
        show_filter()

    if st.button("戻る", width=200):
        st.switch_page("components/home.py")

if st.session_state.take_switch:
    st.session_state.take_switch = False
    st.switch_page("components/game.py")
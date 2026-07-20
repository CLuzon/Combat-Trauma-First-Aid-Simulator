import streamlit as st
import pandas as pd

if "ans" not in st.session_state:
    st.session_state.ans = 0

def close_ex():
    st.session_state.explanation = False
    st.session_state.scenario_cnt += 1
    st.session_state.dev = 0

@st.dialog("解説", width=1200, on_dismiss=close_ex)
def show_explanations(ans, val, table, uni_score):
    ans = int(ans)
    uni_score = int(uni_score)

    st.write(f"選択した答えのスコア：{ans}")
    st.write(val)

    new_table = table.rename(
        columns = {
            "danger_value": "評価",
            "ch_score": "スコア",
            "c_text": "選択肢",
            "e_text": "解説"
        }
    ).copy()

    new_table["スコア"] = (
        pd.to_numeric(new_table["スコア"], errors="coerce").astype("Int64")
    )

    st.write(f"総合スコア: {uni_score}")
    st.table(new_table)
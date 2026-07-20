import streamlit as st
import pandas as pd
from components.field_manual_theme import apply_field_manual_theme
from components.ui_loader import render_html

if "ans" not in st.session_state:
    st.session_state.ans = 0


def close_ex():
    st.session_state.explanation = False
    st.session_state.scenario_cnt += 1
    st.session_state.dev = 0


@st.dialog("処置評価記録", width=1200, on_dismiss=close_ex)
def show_explanations(ans, val, table, uni_score):
    apply_field_manual_theme()
    ans = int(ans)
    uni_score = int(uni_score)

    evaluation_class = (
        "manual-stamp-failure" if val in {"死亡", "悪化"} else "manual-stamp-success"
    )

    render_html(
        "explanation.html", {
            "evaluation_class": evaluation_class,
            "ans": ans,
            "uni_score": uni_score,
            "val": val
        }
    )

    new_table = table.rename(
        columns={
            "danger_value": "評価",
            "ch_score": "スコア",
            "c_text": "選択肢",
            "e_text": "解説",
        }
    ).copy()

    new_table["スコア"] = pd.to_numeric(
        new_table["スコア"], errors="coerce"
    ).astype("Int64")

    st.markdown(
        '<div class="manual-card-label">ALL OPTIONS / 選択肢別の評価記録</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        new_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "選択肢": st.column_config.TextColumn(width="medium"),
            "解説": st.column_config.TextColumn(width="large"),
            "評価": st.column_config.TextColumn(width="small"),
            "スコア": st.column_config.NumberColumn(width="small"),
        },
    )

    st.caption("ダイアログを閉じると、次の記録へ進みます。")

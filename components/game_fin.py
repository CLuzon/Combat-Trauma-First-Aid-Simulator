import streamlit as st
from components.field_manual_theme import apply_field_manual_theme
from components.ui_loader import render_html

if "is_gameover" not in st.session_state:
    st.session_state.is_gameover = True


def close_result():
    st.session_state.tp_id = -1
    st.session_state.is_finish = False
    st.session_state.is_back = True


@st.dialog("訓練結果", width=800, on_dismiss=close_result)
def show_result(score):
    apply_field_manual_theme()
    score = int(score)
    count = int(st.session_state.prev_cnt)
    average = score / count if count > 0 else 0.0

    success = not st.session_state.is_gameover
    stamp_class = "manual-stamp-success" if success else "manual-stamp-failure"
    result_text = "救命成功" if success else "救命失敗"
    result_code = "MISSION COMPLETE" if success else "MISSION FAILED"
    average = f"{score / count:.2f}" if count > 0 else "0.00"

    render_html(
        "game_fin.html", {
            "stamp_class": stamp_class,
            "result_text": result_text,
            "result_code": result_code,
            "average": average,
            "score": score,
            "count": count
        }
    )

    if st.button("訓練記録を閉じてホームへ戻る", width="stretch"):
        close_result()
        st.rerun()

import streamlit as st
from components.field_manual_theme import apply_field_manual_theme

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

    st.markdown(
        f"""
        <div class="manual-code">FINAL TRAINING REPORT / CFA-SIM</div>
        <div class="{stamp_class}">{result_text}</div>
        <div class="manual-card">
          <div class="manual-card-label">{result_code}</div>
          <div class="manual-status">
            <div class="meta-cell"><strong>FINAL SCORE</strong>{score}</div>
            <div class="meta-cell"><strong>AVERAGE</strong>{average:.2f}</div>
            <div class="meta-cell"><strong>DECISIONS</strong>{count}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("訓練記録を閉じてホームへ戻る", width="stretch"):
        close_result()
        st.rerun()

import streamlit as st

if "is_gameover" not in st.session_state:
    st.session_state.is_gameover = True
def close_result():
    st.session_state.tp_id = -1
    st.session_state.is_finish = False
    st.session_state.is_back = True

@st.dialog("結果", width=800, on_dismiss = close_result)
def show_result(score):
    score = int(score)
    count = int(st.session_state.prev_cnt)

    if not st.session_state.is_gameover:
        st.write("[救命成功]")
        st.write("")
    else:
        st.write("[救命失敗]")
    st.write(f"最終スコア：{score}")
    st.write(f'平均スコア：{score / count:.2f}')
    if st.button("ホームに戻る"):
        close_result()
        st.rerun()
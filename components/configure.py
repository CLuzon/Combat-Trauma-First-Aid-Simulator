import streamlit as st



def close_settings():
    st.session_state.dialog_name = None

@st.dialog("設定", width=800, on_dismiss=close_settings)
def show_settings():
    #保留
    #st.button("デザイン")

    if st.button(f"BGM: {st.session_state.volume_mode}"):
        if st.session_state.volume_mode == "ON":
            st.session_state.bgm_on = False
            st.session_state.volume_mode = "OFF"
        else:
            st.session_state.bgm_on = True
            st.session_state.volume_mode = "ON"

        st.rerun()

    #保留
    #st.button("フォントサイズ")

    if st.button("閉じる"):
        st.session_state.dialog_name = None
        st.rerun()
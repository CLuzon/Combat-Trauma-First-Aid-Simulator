import streamlit as st

if "dialog_name" not in st.session_state:
    st.session_state.dialog_name = None
if "confirm_home" not in st.session_state:
    st.session_state.confirm_home = False

def close_menu():
    st.session_state.dialog_name = None
    st.session_state.confirm_home = False

@st.dialog("メニュー", width=800, on_dismiss=close_menu)
def show_menu():
    if st.session_state.confirm_home:
        st.write("ホームに戻ってよろしいですか？")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("はい", key="confirm_home_yes"):
                st.session_state.dialog_name = None
                st.session_state.confirm_home = False
                st.session_state.tp_id = -1

                st.session_state.choice_panel = False
                st.session_state.is_back = True
                st.rerun()
                
        with col2:
            if st.button("いいえ", key="confirm_home_no"):
                st.session_state.confirm_home = False
                st.rerun()

        return

    if st.button("続ける", key="continue"):
        st.session_state.dialog_name = None
        st.rerun()
    
    if st.button("設定", key="settings"):
        st.session_state.dialog_name = "settings"
        st.rerun()
    
    if st.button("ホーム", key="menu_home"):
        st.session_state.confirm_home = True
        st.rerun()
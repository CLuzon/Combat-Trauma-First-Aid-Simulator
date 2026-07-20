import streamlit as st
from components.dictionary import show_dictionary
from components.configure import show_settings
from components.ui_loader import load_css, render_html

if "volume_mode" not in st.session_state:
    st.session_state.volume_mode = "OFF"

if "bgm_on" not in st.session_state:
    st.session_state.bgm_on = False

st.set_page_config(
    page_title="戦闘外傷救護シミュレーター",
    page_icon="★",
    layout="centered",
)

load_css("home.css")


@st.dialog("出典")
def show_sources():
    st.markdown("**[テキスト]**")
    st.write("イラストでまなぶ！ 戦闘外傷救護-COMBAT FIRST AID-")
    st.write("著者：照井資規")
    st.markdown("**[BGM]**")
    st.write("Given Up - Linkin Park")
    st.write("Do I Wanna Know - Arctic Monkeys")
    st.write("GASOLINE - Måneskin")
    st.write("OWN MY MIND - Måneskin")
    st.markdown("**[SE]**")
    st.markdown("[効果音ラボ](https://soundeffect-lab.info/)")
    st.markdown("**[使用AI]**")
    st.write("ChatGPT")


render_html(
    "home.html",
    {
        "document_code": "FIELD MEDICAL TRAINING MANUAL / MODULE SELECT",
        "title": "訓練モードを選択",
        "description": "無作為にシナリオを開始するか、索引から特定の訓練記録を指定すること。",
        "classification": "TRAINING MODE",
    }
)

with st.container(horizontal_alignment="center"):
    if st.button("01 ゲーム開始", width=200):
        st.switch_page("components/prepare_game.py")

    if st.button("02 辞書", width=200):
        show_dictionary()

    if st.button("03 設定", width=200):
        show_settings()

    if st.button("04 出典", width=200):
        show_sources()

st.markdown('<div class="manual-note">COMPLETE EACH MODULE IN THE ORDER PRESENTED</div>', unsafe_allow_html=True)

if st.session_state.bgm_on:
    st.audio(
        "bgm/given_up.mp3",
        format="audio/mpeg",
        autoplay=True,
        loop=True,
    )

import streamlit as st
from components.dictionary import show_dictionary
from components.configure import show_settings

if "volume_mode" not in st.session_state:
    st.session_state.volume_mode = "OFF"

if "bgm_on" not in st.session_state:
    st.session_state.bgm_on = False

st.set_page_config(
    page_title = "戦闘外傷救護シミュレーター",
    layout="centered"
)

@st.dialog("出典")
def show_sources():
    st.write("[テキスト]")
    st.write("イラストでまなぶ！ 戦闘外傷救護-COMBAT FIRST AID-")
    st.write("著者：照井資規")
    st.write(" ")
    st.write("[BGM]")
    st.write("Given Up - Linkin Park")
    st.write("Do I Wanna Know - Arctic Monkeys")
    st.write("GASOLINE - Maneskin")
    st.write("OWN MY MIND - Maneskin")
    st.write("[SE]")
    st.write("効果音ラボ(https://soundeffect-lab.info/)")
    st.write(" ")
    st.write("[使用AI]")
    st.write("chatGPT")
    

st.subheader(
    "戦闘外傷救護シミュレーター",
    text_alignment="center"
)

with st.container(
    width="stretch",
    horizontal_alignment="center"
):
    if st.button("ゲーム開始", width=200):
        st.switch_page("components/prepare_game.py")

    if st.button("辞書", width=200):
        show_dictionary()

    if st.button("設定", width=200):
        show_settings()

    if st.button("出典", width=200):
        show_sources()



if st.session_state.bgm_on:
    st.audio(
        "bgm/given_up.mp3",
        format="audio/mpeg",
        autoplay=True,
        loop=True
    )

st.html("""
<style>
    [data-testid="stAudio"] {
        display: none;
    }
</style>
""")
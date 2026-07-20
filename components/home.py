import streamlit as st
from components.dictionary import show_dictionary
from components.configure import show_settings

if "volume_mode" not in st.session_state:
    st.session_state.volume_mode = "OFF"

if "bgm_on" not in st.session_state:
    st.session_state.bgm_on = False

st.set_page_config(
    page_title="戦闘外傷救護シミュレーター",
    page_icon="★",
    layout="centered",
)

st.html("""
<style>
:root {
    --paper: #c9bf9d;
    --paper-light: #ded5b7;
    --ink: #24271f;
    --olive: #4b5338;
    --olive-dark: #303725;
    --stamp: #8b342d;
    --line: rgba(36,39,31,.55);
}

.stApp {
    background:
        repeating-linear-gradient(0deg, rgba(40,42,32,.025) 0, rgba(40,42,32,.025) 1px, transparent 1px, transparent 4px),
        radial-gradient(circle at 50% 15%, #77755f 0%, #44483a 52%, #292d25 100%);
    color: var(--ink);
}

.block-container {
    max-width: 760px;
    padding-top: 3.2rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

.manual-sheet {
    position: relative;
    padding: 1.1rem;
    background: var(--paper);
    border: 2px solid var(--ink);
    box-shadow: 11px 13px 0 rgba(18,21,16,.32), 0 25px 70px rgba(0,0,0,.28);
}

.manual-sheet::before {
    content: "FOR TRAINING USE";
    position: absolute;
    right: 1rem;
    top: .8rem;
    padding: .25rem .55rem;
    border: 2px solid var(--stamp);
    color: var(--stamp);
    font-weight: 900;
    font-size: .66rem;
    letter-spacing: .12em;
    transform: rotate(2deg);
    opacity: .9;
}

.manual-border {
    border: 1px solid var(--ink);
    padding: 1.6rem 1.35rem 1.2rem;
    background:
      linear-gradient(rgba(255,255,255,.08), rgba(255,255,255,.08)),
      repeating-linear-gradient(90deg, transparent, transparent 34px, rgba(55,57,44,.025) 35px);
}

.manual-code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: .7rem;
    letter-spacing: .13em;
    color: var(--olive-dark);
    border-bottom: 1px solid var(--line);
    padding-bottom: .7rem;
}

.manual-title {
    margin: 1.6rem 0 .65rem;
    font-size: clamp(1.6rem, 4vw, 2.35rem);
    line-height: 1.25;
    color: var(--ink);
    font-weight: 900;
    letter-spacing: .035em;
}

.manual-subtitle {
    max-width: 32rem;
    color: #45483b;
    font-size: .93rem;
    line-height: 1.75;
}

.manual-rule {
    display: flex;
    align-items: center;
    gap: .7rem;
    margin-top: 1.4rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .12em;
}
.manual-rule::before, .manual-rule::after {
    content: "";
    height: 1px;
    background: var(--ink);
    flex: 1;
}

.manual-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .55rem;
    margin-top: 1rem;
}
.meta-cell {
    border: 1px solid var(--line);
    padding: .58rem .65rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: .69rem;
}
.meta-cell strong { display:block; font-size:.62rem; color:#585b4d; margin-bottom:.2rem; letter-spacing:.08em; }

.stButton > button {
    width: 200px;
    min-height: 46px;
    border-radius: 0;
    border: 2px solid var(--ink);
    background: var(--paper-light);
    color: var(--ink);
    font-weight: 850;
    letter-spacing: .07em;
    box-shadow: 4px 4px 0 var(--olive-dark);
    transition: .12s ease;
}

.stButton > button:hover {
    background: var(--olive);
    color: #f0ead3;
    border-color: var(--ink);
    transform: translate(1px, 1px);
    box-shadow: 2px 2px 0 var(--olive-dark);
}

.stButton > button:focus:not(:active) {
    color: var(--ink);
    border-color: var(--ink);
}

.manual-note {
    text-align:center;
    margin-top:1.2rem;
    color:#d8d3ba;
    font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size:.68rem;
    letter-spacing:.12em;
}

[data-testid="stDialog"] > div {
    background: var(--paper-light) !important;
    border: 2px solid var(--ink);
    border-radius: 0 !important;
    color: var(--ink);
}
[data-testid="stDialog"] h2,
[data-testid="stDialog"] p,
[data-testid="stDialog"] div { color: var(--ink); }

[data-testid="stAudio"] { display: none; }

@media (max-width: 640px) {
    .block-container { padding-top: 1.2rem; }
    .manual-sheet::before { position: static; display:inline-block; margin-bottom:.5rem; }
    .manual-meta { grid-template-columns: 1fr; }
}
</style>
""")


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


st.markdown("""
<div class="manual-sheet">
  <div class="manual-border">
    <div class="manual-code">FIELD MEDICAL TRAINING MANUAL / MODULE 00</div>
    <h1 class="manual-title">戦闘外傷救護<br>シミュレーター</h1>
    <div class="manual-subtitle">
      戦闘環境下で発生する外傷に対し、状況評価・救護・搬送の判断を訓練する。
      各設問では、脅威と負傷者の状態を確認し、最も適切な行動を選択すること。
    </div>
    <div class="manual-rule">MISSION MENU</div>
    <div class="manual-meta">
      <div class="meta-cell"><strong>CLASSIFICATION</strong>TRAINING</div>
      <div class="meta-cell"><strong>DOCUMENT</strong>CFA-SIM-01</div>
      <div class="meta-cell"><strong>REVISION</strong>2026 / 07</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

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

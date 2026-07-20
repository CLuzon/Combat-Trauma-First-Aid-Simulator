### import群
import streamlit as st
import pandas as pd
from components.menu import show_menu
from components.dictionary import show_dictionary
from components.configure import show_settings
from components.explanation import show_explanations
from components.game_fin import show_result
from components.field_manual_theme import apply_field_manual_theme, manual_header

### Excel群
tp_df = pd.read_excel("db/stories.xlsx", sheet_name="topic")
sr_df = pd.read_excel("db/stories.xlsx", sheet_name="scenario")
qs_df = pd.read_excel("db/stories.xlsx", sheet_name="question")
ch_df = pd.read_excel("db/stories.xlsx", sheet_name="choice")

### session_state群
if "ans" not in st.session_state:
    st.session_state.ans = None
if "choice_panel" not in st.session_state:
    st.session_state.choice_panel = False
if "dialog_name" not in st.session_state:
    st.session_state.dialog_name = None
elif st.session_state.dialog_name == "settings":
    show_settings()
else:
    st.session_state.dialog_name = None
if "confirm_home" not in st.session_state:
    st.session_state.confirm_home = False
elif st.session_state.confirm_home is True:
    show_menu()
else:
    st.session_state.dialog_name = False
if "dev" not in st.session_state:
    st.session_state.dev = 0
if "tp_id" not in st.session_state:
    st.session_state.tp_id = -1
if "ch_table" not in st.session_state:
    st.session_state.ch_table = None
if "check" not in st.session_state:
    st.session_state.check = False
if "explanation" not in st.session_state:
    st.session_state.explanation = False
if "ans_score" not in st.session_state:
    st.session_state.ans_score = 0
if "value_score" not in st.session_state:
    st.session_state.value_score = 0
if "next_tp_id" not in st.session_state:
    st.session_state.next_tp_id = None
if "scenario_cnt" not in st.session_state:
    st.session_state.scenario_cnt = 0
if "prev_cnt" not in st.session_state:
    st.session_state.prev_cnt = 0
if "uni_score" not in st.session_state:
    st.session_state.uni_score = 0
if "is_finish" not in st.session_state:
    st.session_state.is_finish = False
if "is_back" not in st.session_state:
    st.session_state.is_back = False
if "is_gameover" not in st.session_state:
    st.session_state.is_gameover = False
if "danger_level" not in st.session_state:
    st.session_state.danger_level = 3
if "filter_id" not in st.session_state:
    st.session_state.filter_id = None
if "bgm_on" not in st.session_state:
    st.session_state.bgm_on = False
if "prev_score" not in st.session_state:
    st.session_state.prev_score = 0
if "get_next" not in st.session_state:
    st.session_state.get_next = None


def initialize():
    st.session_state.choice_panel = False
    st.session_state.ans = None
    st.session_state.dev = 0
    st.session_state.tp_id = -1
    st.session_state.ch_table = None
    st.session_state.check = False
    st.session_state.explanation = False
    st.session_state.ans_score = 0
    st.session_state.value_score = 0
    st.session_state.next_tp_id = None
    st.session_state.scenario_cnt = 0
    st.session_state.prev_cnt = 0
    st.session_state.uni_score = 0
    st.session_state.is_finish = False
    st.session_state.is_gameover = False


def check_ch():
    anss = st.session_state.ans
    if anss is None:
        return

    st.session_state.ans_score = anss["ch_score"]
    st.session_state.value_score = anss["danger_value"]
    st.session_state.uni_score += st.session_state.ans_score
    st.session_state.prev_score = st.session_state.ans_score
    st.session_state.explanation = True
    st.session_state.check = False

    if st.session_state.value_score == "死亡":
        st.session_state.is_finish = True
        st.session_state.is_gameover = True


def choice_text():
    tp = st.session_state.tp_id
    qs = qs_df.loc[qs_df["id_tp"] == tp]

    if qs.empty:
        st.markdown('<div class="manual-card">＊＊＊</div>', unsafe_allow_html=True)
        st.session_state.is_finish = True
        return

    qs_id = qs.iloc[0]["id_qs"]
    ch = ch_df.loc[ch_df["id_qs"] == qs_id]
    if ch.empty:
        return

    st.session_state.ch_table = ch.drop(columns=["id_ch", "id_qs"])

    st.markdown(
        f"""
        <div class="manual-card">
          <div class="manual-card-label">DECISION REQUIRED / 設問</div>
          <strong>{qs.iloc[0]['q_text']}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True, width="stretch", horizontal_alignment="center"):
        st.caption("ACTION OPTIONS / 行動を選択")
        for i in range(len(ch)):
            choice = ch.iloc[i]
            if st.button(
                f"{i + 1:02d}　{choice['c_text']}",
                key=f"choice_{qs_id}_{i}",
                width=420,
            ):
                st.session_state.ans = choice
                st.session_state.choice_panel = False
                st.session_state.check = True
                st.rerun()


def main_text():
    if st.session_state.tp_id == -1:
        if st.session_state.filter_id is None:
            candidates = tp_df[tp_df["prog"] == 0]
            if candidates.empty:
                return
            st.session_state.tp_id = candidates.sample(n=1)["id_tp"].iloc[0]
        else:
            st.session_state.tp_id = st.session_state.filter_id

        st.session_state.ans = None
        st.session_state.scenario_cnt = 0
        st.session_state.prev_cnt = 0
        st.session_state.uni_score = 0
        st.session_state.dev = 0
        st.session_state.get_next = tp_df[
            tp_df["parent_value"] == st.session_state.tp_id
        ]

    if st.session_state.scenario_cnt != st.session_state.prev_cnt:
        st.session_state.prev_cnt = st.session_state.scenario_cnt

        if not st.session_state.get_next.empty:
            tmp_table = st.session_state.get_next.iloc[0:0]
            while tmp_table.empty and st.session_state.prev_score <= 5:
                tmp_table = st.session_state.get_next.loc[
                    st.session_state.get_next["entry_score"]
                    == st.session_state.prev_score
                ]
                st.session_state.prev_score += 1

            if not tmp_table.empty:
                st.session_state.next_tp_id = tmp_table.sample(n=1)["id_tp"].iloc[0]
            else:
                st.session_state.next_tp_id = -1
        else:
            st.session_state.next_tp_id = -1

        st.session_state.tp_id = st.session_state.next_tp_id
        st.session_state.get_next = tp_df[
            tp_df["parent_value"] == st.session_state.tp_id
        ]
        st.session_state.ans = None
        st.session_state.dev = 0

    if st.session_state.tp_id == -1:
        st.session_state.is_finish = True

    tp = st.session_state.tp_id
    dev = st.session_state.dev
    tp_sr = sr_df.loc[sr_df["id_tp"] == tp]
    tmp = tp_sr.loc[tp_sr["part_prog"] == dev, "s_text"]

    if not tmp.empty:
        st.markdown(
            f"""
            <div class="manual-card">
              <div class="manual-card-label">FIELD REPORT / TOPIC {tp} / PAGE {dev + 1:02d}</div>
              <div style="line-height:1.9;">{tmp.iloc[0]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("次頁 ▶", key=f"next_{tp}_{dev}", width="stretch"):
                st.session_state.dev += 1
                st.rerun()
    elif st.session_state.ans is None:
        st.session_state.choice_panel = True


if st.session_state.is_back:
    initialize()
    st.session_state.is_back = False
    st.switch_page("components/home.py")

st.set_page_config(
    page_title="戦闘外傷救護シミュレーター",
    page_icon="✚",
    layout="centered",
)
apply_field_manual_theme()
manual_header(
    "FIELD MEDICAL TRAINING MANUAL / ACTIVE SCENARIO",
    "戦闘外傷救護シミュレーター",
    "状況報告を読み、脅威・傷病者・任務を同時に評価して行動を決定すること。",
    "SCENARIO RECORD",
)

with st.container(width="stretch", horizontal_alignment="center"):
    main_text()
    if st.session_state.choice_panel:
        choice_text()

st.markdown(
    f"""
    <div class="manual-status">
      <div class="meta-cell"><strong>TOPIC</strong>{st.session_state.tp_id}</div>
      <div class="meta-cell"><strong>RECORD</strong>{st.session_state.scenario_cnt}</div>
      <div class="meta-cell"><strong>SCORE</strong>{int(st.session_state.uni_score)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("メニュー", width="stretch"):
        show_menu()
with col2:
    if st.button("辞書", width="stretch"):
        show_dictionary()

if st.session_state.check:
    check_ch()

if st.session_state.explanation:
    show_explanations(
        st.session_state.ans_score,
        st.session_state.value_score,
        st.session_state.ch_table,
        st.session_state.uni_score,
    )
elif st.session_state.is_finish:
    show_result(st.session_state.uni_score)
else:
    st.session_state.explanation = False

if st.session_state.bgm_on:
    st.audio(
        "bgm/own_my_mind.mp3",
        format="audio/mpeg",
        autoplay=True,
        loop=True,
    )

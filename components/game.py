###import群
import streamlit as st
import pandas as pd
from components.menu import show_menu
from components.dictionary import show_dictionary
from components.configure import show_settings
from components.explanation import show_explanations
from components.game_fin import show_result

###Excel群
tp_df = pd.read_excel("db/stories.xlsx", sheet_name="topic")
sr_df = pd.read_excel("db/stories.xlsx", sheet_name="scenario")
qs_df = pd.read_excel("db/stories.xlsx", sheet_name="question")
ch_df = pd.read_excel("db/stories.xlsx", sheet_name="choice")


###session_state群
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
elif st.session_state.confirm_home == True:
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
    st.session_state.is_finish  = False

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
###

###def群
def initialize():
    st.session_state.choice_panel = False #選択肢呼び出しの初期化
    st.session_state.ans = None #回答の初期化
    st.session_state.dev = 0 #テキスト進行の初期化
    st.session_state.tp_id = -1 #topicの初期化
    st.session_state.ch_table = None #選択テーブルの初期化
    st.session_state.check = False #チェックの初期化
    st.session_state.explanation = False #解説の初期化
    st.session_state.ans_score = 0 #スコアの初期化
    st.session_state.value_score = 0 #重要度の初期化
    st.session_state.next_tp_id = None #次のトピックの初期化
    st.session_state.scenario_cnt = 0 #シナリオ進行の初期化
    st.session_state.prev_cnt = 0 #過去シナリオの初期化
    st.session_state.uni_score = 0 #総合スコアの初期化
    st.session_state.is_finish  = False #完了初期化
    st.session_state.is_gameover = False #ゲームオーバー初期化

#1トピックの審議
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
        st.write("ゲームオーバー")
        st.session_state.is_finish = True
        st.session_state.is_gameover = True

#選択肢
def choice_text():
    tp = st.session_state.tp_id

    qs = qs_df.loc[qs_df["id_tp"] == tp]
    if qs.empty:
        st.write("＊＊＊")
        st.session_state.is_finish = True
        return
    
    qs_id = qs.iloc[0]["id_qs"]
    ch = ch_df.loc[ch_df["id_qs"] == qs_id]
    if ch.empty:
        return
    
    st.session_state.ch_table = ch.drop(columns=["id_ch", "id_qs"])
    
    with st.container(
        border=True,
        width="stretch",
        horizontal_alignment="center"
    ):
        st.write(qs.iloc[0]["q_text"])
    
    with st.container(
        border=True,
        width="stretch",
        horizontal_alignment="center"
    ):
        for i in range(len(ch)):
            choice = ch.iloc[i]

            if st.button(
                f"{choice['c_text']}",
                key = f"choice_{qs_id}_{i}",
                width=250
            ):
                st.session_state.ans = choice
                st.session_state.choice_panel = False
                st.session_state.check = True
                st.rerun()



#トピック表示
def main_text():
    #topicがない場合
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

        #topicの続きを設定
        st.session_state.get_next = tp_df[tp_df["parent_value"] == st.session_state.tp_id]


    #現在のカウントと過去のカウントが異なるときにストーリーの進捗を進める 
    if st.session_state.scenario_cnt != st.session_state.prev_cnt:
        st.session_state.prev_cnt = st.session_state.scenario_cnt #prev=scenario

        #late
        if not st.session_state.get_next.empty:
            tmp_table = st.session_state.get_next.iloc[0:0]
            while tmp_table.empty and st.session_state.prev_score <= 5:
                tmp_table = st.session_state.get_next.loc[st.session_state.get_next["entry_score"] == st.session_state.prev_score]
                st.session_state.prev_score += 1

            if not tmp_table.empty:
                st.session_state.next_tp_id = tmp_table.sample(n=1)["id_tp"].iloc[0]
            else:
                st.session_state.next_tp_id = -1
        else:
            st.session_state.next_tp_id = -1

        st.session_state.tp_id = st.session_state.next_tp_id #tp_id <- next_tp_id
        
        st.session_state.get_next = tp_df[tp_df["parent_value"] == st.session_state.tp_id]

        st.session_state.ans = None #ansを取り消す
        st.session_state.dev = 0
        

    if st.session_state.tp_id == -1:
        st.session_state.is_finish = True
    
    tp = st.session_state.tp_id
    dev = st.session_state.dev
    
    tp_sr = sr_df.loc[sr_df["id_tp"] == tp]

    tmp = tp_sr.loc[tp_sr["part_prog"] == dev, "s_text"]
    
    if not tmp.empty:
        with st.container(
            border=True,
            width="stretch"
        ):
            st.write(tmp.iloc[0])

        col1, col2 = st.columns([9,1])
        with col2:
            if st.button("進む", key=f"next_{tp}_{dev}"):
                st.session_state.dev += 1
                st.rerun()
    else:
        if st.session_state.ans is None:
            st.session_state.choice_panel = True



    
###ホームへ移動
if st.session_state.is_back:
    initialize()
    st.session_state.is_back = False
    st.switch_page("components/home.py")


###Widget
st.set_page_config(
    page_title="戦闘外傷救護シミュレーター",
    layout = "centered"
)

st.subheader(
    "戦闘外傷救護シミュレーター",
    text_alignment="center"
)
#テキスト表示
with st.container(
    width="stretch",
    horizontal_alignment="center"
):
    main_text()
    #選択肢表示
    if st.session_state.choice_panel:
        choice_text()


col1, col2 = st.columns([1,5])

with col1:
    with st.container(
    width="stretch",
    horizontal_alignment="center"
    ):
        if st.button("メニュー", width=100):
            show_menu()
        if st.button("辞書", width=100):
            show_dictionary()


###その他
if st.session_state.check:
    check_ch()

if st.session_state.explanation:
    show_explanations(
        st.session_state.ans_score,
        st.session_state.value_score,
        st.session_state.ch_table,
        st.session_state.uni_score
    )
elif st.session_state.is_finish:
    show_result(st.session_state.uni_score)
else:
    st.session_state.explanation = False

    
###BGM
if st.session_state.bgm_on:
    st.audio(
        "bgm/own_my_mind.mp3",
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

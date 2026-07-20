import streamlit as st

home_page = st.Page(
    "components/home.py",
    title="Home",
    default = True
)

game_page = st.Page(
    "components/game.py",
    title = "Game"
)

prepare_game = st.Page(
    "components/prepare_game.py",
    title = "Prepare"
)

page = st.navigation(
    [home_page, game_page, prepare_game],
    position = "hidden"
 )
page.run()

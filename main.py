import streamlit as st
import pandas as pd

from backend.recommender import recMusics

TITLE = "SongTrx"

songs = pd.read_csv('resources/tcc_ceds_music.csv')

songs = songs[["artist_name", "track_name", "genre"]]

songs["songs"] = songs["track_name"] + "-" + songs["artist_name"]

st.set_page_config(
    page_title=TITLE, page_icon=":bar_chart:", layout="centered"
)

st.title(TITLE)
st.markdown('##')

with st.sidebar.expander("Age", expanded=True):
    age = st.slider("Select your age:", 0, 120)

with st.sidebar.expander("Songs You Like", expanded=True):
    songs = st.multiselect(
        "Select your favorate songs:",
        options=songs["songs"].unique()
        )
    
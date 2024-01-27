import streamlit as st

from backend.recommender import recMusics

TITLE = "SongTrx"

st.set_page_config(
    page_title=TITLE, page_icon=":bar_chart:", layout="centered"
)

st.title(TITLE)
st.markdown('##')

with st.sidebar.expander("Age", expanded=True):
    age = st.slider("Select your age:", 0, 120)
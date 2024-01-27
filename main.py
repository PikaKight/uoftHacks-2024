import os
import streamlit as st
import pandas as pd

from backend.recommender import recMusics
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv('.env')

TITLE = "SongTrx"

songs = pd.read_csv('resources/tcc_ceds_music.csv')

songs = songs[["artist_name", "track_name", "genre"]]

songs["songs"] = songs["track_name"] + " by " + songs["artist_name"]

songList = songs["songs"].to_list()
genreList = list(set(songs['genre'].to_list()))


def getVid(title):
    yt = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE"))

    search = yt.search().list(
        q=title,
        part='id',
        type='video',
        maxResults=1
    ).execute()

    items = search.get('items', [])
    if items:
        video_id = items[0]['id']['videoId']
        return video_id
    else:
        return None

def itemCard(titles):
    length = len(titles)
    i = 0
    while i < length:
        row = st.columns(3)
    
        for col in row:
            card = col.container(height=300, border=True)

            print(titles[i])
            
            video_id = getVid(titles[i])

            if video_id:
                with card:
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
            else:
                with card:
                    st.warning("Video Not Found")

            with card:
                st.write(titles[i])

            if (i+2) < length:
                i += 1

            else:
                break
        
        i +=1 

st.set_page_config(
    page_title=TITLE, page_icon=":bar_chart:", layout="centered"
)

st.title(TITLE)
st.markdown('##')

with st.sidebar.expander("Number of Songs", expanded=True):
    numSongs = st.slider("Number of Songs Suggestions:", 0, 20)

with st.sidebar.expander("Age", expanded=True):
    age = st.slider("Select your age:", 0, 120)

with st.sidebar.expander("Songs You Like", expanded=True):
    song = st.multiselect(
        "Select your favorate songs:",
        options=songList
        )
    


with st.sidebar.expander("Genres You Like", expanded=True):
    genre = st.multiselect(
        "Select your favorite Genres:",
        options=genreList
    )

if st.sidebar.button("Search"):
    suggestions = recMusics(numSongs, age, song, genre)

    itemCard(suggestions)


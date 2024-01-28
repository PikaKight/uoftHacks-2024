import os
import streamlit as st
import pandas as pd

from backend.recommender import recMusics
from backend.data import getAllGenre, getAllSongs, addGenre, addSong
from backend.musicGen import genMelody
from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv('.env')

TITLE = "SongTrx"

songList = getAllSongs()
genreList = getAllGenre()


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
    x = 0
    while i < length:
        row = st.columns(3)
    
        for col in row:
            card = col.container(height=400, border=True)

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

            if x < 2 and i < length -1:
                i += 1
                x += 1

            else:
                x=0
                break
        
        i +=1 

logo = "./resources/songtrx logo.png"

st.set_page_config(
    page_title=TITLE, page_icon=logo, layout="centered"
)

st.image(logo, width=300)
st.title(TITLE)
st.markdown('##')

# memory = st.text_area("Please Enter a Memory for a Melody:")

# if memory:
#     melody = genMelody(memory)

#     st.write("Generated Melody:")
#     melody.show('midi')

with st.sidebar.expander("Number of Songs", expanded=True):
    numSongs = st.slider("Number of Songs Suggestions:", 0, 20)

with st.sidebar.expander("Age", expanded=True):
    age = st.slider("Select your age:", 0, 120)

with st.sidebar.expander("Songs You Like", expanded=True):
    song = st.multiselect(
        "Select your favorate songs:",
        options=songList
        )
    
    newSong = st.text_input("If Song not found, please enter with using [Song Name by Artist] format")

    if newSong not in songList and newSong != "":
        print(newSong)
        addSong(newSong)

    elif newSong in songList and newSong != "":
        st.warning("Song already exist")

with st.sidebar.expander("Genres You Like", expanded=True):
    genre = st.multiselect(
        "Select your favorite Genres:",
        options=genreList
    )

    newGenre = st.text_input("If Genre not found, please enter genre")

    if newGenre not in genreList and newGenre != "":
        print(newGenre)
        addGenre(newGenre)

    elif newGenre in genreList and newGenre != "":
        st.warning("Genre already exist")

st.sidebar.write("Please Press the Refresh Button to see the added Song or Genre.")

if st.sidebar.button("Refresh"):
        pass

if st.sidebar.button("Search"):
        suggestions = recMusics(numSongs, age, song, genre)
        itemCard(suggestions)




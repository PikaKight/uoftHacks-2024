import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import pandas as pd


load_dotenv('.env')

client = MongoClient(os.getenv("MONGO"), server_api=ServerApi('1'))

db = client['SongTrx']

songs = db['Songs']
genres = db['Genre']
users = db['Users']

def saveSongs(songList: list) -> None:

    for song in songList:
        songs.insert_one({
            "Song": song
        })

def saveGenres(genreList: list) -> None:
    
    for genre in genreList:
        genres.insert_one({
            "Genre": genre
        })

def getAllSongs() -> list:

    songList = []

    songRes = [x for x in songs.find()]

    for song in songRes:
        songList.append(song["Song"])
        
    return songList

def getAllGenre() -> list:

    genreList = []
    genreRes = [x for x in genres.find()]

    for genre in genreRes:
        genreList.append(genre['Genre'])

    return genreList

def addSong(title) -> None:

    if songs.find_one({"Song": title}):
        return

    songs.insert_one({
        "Song": title
    })

def addGenre(genre) -> None:

    if genres.find_one({"Genre": genre}):
        return

    genres.insert_one({
        "Genre": genre
    })


if __name__ == ("__main__"):
    song = pd.read_csv('resources/tcc_ceds_music.csv')
    song = song[["artist_name", "track_name", "genre"]]

    song["songs"] = song["track_name"] + " by " + song["artist_name"]

    songList = song["songs"].to_list()
    genreList = list(set(song['genre'].to_list()))

    # saveGenres(genreList)
    # saveSongs(songList)

    
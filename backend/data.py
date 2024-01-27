import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

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

    songRes = songs.find()

    for key, value in songRes.items():
        songList.append(value)


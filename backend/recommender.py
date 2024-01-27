import cohere
import os
import re

from datetime import datetime
from dotenv import load_dotenv

load_dotenv('.env')

co = cohere.Client(os.getenv('COHERE'))

CHILDHOOD = [3, 12]


def recMusics(numSongs:int, age: int, songs: list, genres: list) -> list:
    cYear = datetime.now().year
    
    yearRang = f"{cYear - (age - CHILDHOOD[0])} to {cYear - (age - CHILDHOOD[1])}"
    song = ', '.join(songs)
    genre = ', '.join(genres)
    
    msg = f"What are {numSongs} different popular songs from {yearRang} that are similar to, but not the {song} and similar genre to {genre}. Please have the list of songs formated using the template delimitted by single quotation marks 'Year: Song Name: Artist Name'. Do not include the template in the list."

    print(msg)

    res = co.chat(message=msg, connectors=[{'id': 'web-search'}], citation_quality='fast')

    pattern = r'[\d]+\.+(.*)'

    res = re.findall(pattern, res.text)

    return res[:numSongs]


if __name__ == "__main__":
    numSongs = 10
    age = 21
    songs = ["Believer - Imagine Dragon", "Pop Star - KDA"]
    genres = ["Pop", "KPop", "JPop", "MandoPop"]

    res = recMusics(numSongs, age, songs, genres)

    print(res)
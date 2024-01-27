import cohere
import os
import re
import json

from datetime import datetime
from dotenv import load_dotenv
from cohere.responses.classify import Example

load_dotenv('.env')

co = cohere.Client(os.getenv('COHERE'))

CHILDHOOD = [3, 12]


def recMusics(numSongs:int, age: int, songs: list, genres: list) -> list:
    cYear = datetime.now().year
    
    yearRang = f"{cYear - (age - CHILDHOOD[0])} to {cYear - (age - CHILDHOOD[1])}"
    song = ', '.join(songs)
    genre = ', '.join(genres)
    
    msg = f"What are {numSongs} different popular songs from {yearRang} that are similar to, but not the {song} and similar genre to {genre}. Please have the numbered list of songs formated using the template delimitted by single quotation marks 'Year: Song Name: Artist Name'. Do not include the template in the list."

    print(msg)

    res = co.chat(message=msg, connectors=[{'id': 'web-search'}], citation_quality='fast')

    print(res.text)

    pattern = r'[\d]+\.+(.*)'

    res = re.findall(pattern, res.text)

    print(res)

    return res[:numSongs]


def memoryCat(training, memory):
    example = []
    for i in training:
        example.append(Example(i["text"], i["label"]))

    res = co.classify(
        inputs=memory,
        examples=example)

    return res.classifications
    

if __name__ == "__main__":
    # numSongs = 10
    # age = 21
    # songs = ["Believer - Imagine Dragon", "Pop Star - KDA"]
    # genres = ["Pop", "KPop", "JPop", "MandoPop"]

    # res = recMusics(numSongs, age, songs, genres)

    jsonEx = open("./model/memory/training.json", 'r')
    example = json.load(jsonEx)
    memory = [
        "It was a warm summer day, and the air was filled with the scent of pine trees as my family and I embarked on a camping trip to a picturesque national park. The anticipation and excitement were palpable as we loaded up the car with a tent, sleeping bags, and a cooler filled with snacks. I could hardly contain my enthusiasm as I imagined the adventures that awaited us.  Upon reaching the campsite, we set up our tent amidst a lush green clearing surrounded by towering trees. The sound of birds chirping and the gentle rustle of leaves overhead created a tranquil atmosphere. I remember helping my parents stake down the tent and feeling a sense of accomplishment as it stood proudly against the backdrop of nature.  As evening approached, we gathered around the campfire, the warmth of the flames contrasting with the cool night air. We roasted marshmallows to perfection, the golden brown exterior giving way to gooey sweetness inside. The laughter and chatter around the campfire created a sense of togetherness that is etched into my memory.  Underneath the starlit sky, my family and I huddled together inside the tent, sharing stories and jokes by the dim light of a lantern. The rhythmic sounds of crickets and distant owls provided a soothing lullaby, making it easy to drift into a peaceful slumber.  The next morning, we awoke to the gentle rays of the sun filtering through the tent fabric. The aroma of a simple but hearty breakfast being prepared over a portable stove wafted through the air. I can vividly recall the taste of scrambled eggs and bacon, savoring each bite as we sat on foldable chairs overlooking a serene lake.  During the day, we explored the trails that led us deeper into the heart of the forest. We discovered hidden streams, vibrant wildflowers, and the thrill of spotting a deer grazing in the distance. Every step felt like an adventure, and the simplicity of nature became a source of pure joy.  As the camping trip came to an end, I realized that it wasn't just about the destination but the shared moments, laughter, and connection with my family. That camping adventure remains a cherished memory, a testament to the beauty of spending quality time together in the great outdoors.",
        "As a child, I vividly remember the bittersweet experience of leaving our family home, a place filled with countless happy memories. My parents had decided to move to a different city for better job opportunities, and it meant saying goodbye to the house that had been our sanctuary for many years.  The packing process was a mix of joy and nostalgia. Every item held a story - from the crayon drawings on the kitchen wall to the marks on the doorframe that tracked my height over the years. We stumbled upon old photo albums, triggering laughter as we reminisced about birthdays, holidays, and family gatherings. The joy of reliving those moments mingled with the sadness of knowing they were part of the past.  On the last night in our home, we gathered in the living room, surrounded by half-packed boxes and the echo of empty rooms. We shared stories, jokes, and our favorite memories. The atmosphere was both celebratory and melancholic, as we celebrated the wonderful times we had in the house while mourning the inevitable farewell.  As the sun set on the familiar neighborhood, we took a final walk around the backyard, remembering the countless games played and the laughter that echoed in those spaces. The warmth of the memories collided with the cold reality of leaving it all behind.  The next morning, we drove away from our childhood home. Watching it disappear in the rearview mirror brought tears to our eyes, but there was also a sense of anticipation for the new adventures that awaited us. The mix of happiness for the memories we carried with us and sadness for the chapter we closed made the farewell unforgettable. In that moment, the nostalgia of the past and the excitement of the future were intertwined, creating a complex tapestry of emotions that defined that bittersweet memory."
        ]

    res = memoryCat(example, memory)

    print(res)
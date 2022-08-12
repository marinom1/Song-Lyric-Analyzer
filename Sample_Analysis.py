import json
from functionDefinitions import *
with open('Lyrics_Khalid_all.json') as json_file:
    data = json.load(json_file)

c = Counter()
analyze_song(data, 1)

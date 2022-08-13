import json
from functionDefinitions import *

# Lyrics_Khalid_all.json was created as a result of using lyricsgenius search_artist function
with open('Lyrics_Khalid_all.json') as json_file:
    data = json.load(json_file)

# Give the data to the analyze_Song function along with the index of the song we want to analyze,
analyze_song(data, 1)

"""
The output from executing this file will be:

Song name: Young Dumb & Broke
Primary Artist: Khalid
Featured Artists: []
Total Words In Song: 266
Number Of Unique Words In Song: 72
Uniqueness Percent Of Song: 27.0677%
5 Most Repeated Words In The Song: [('young', 38), ('dumb', 29), ('broke', 18), ('and', 13), ('high', 8)]
5 Most Repeated Nouns In The Song: [('school', 6), ('kids', 6), ('love', 4), ('moment', 2), ('name', 2)]
5 Most Repeated Adjectives In The Song: [('dumb', 23), ('Young', 17), ('young', 15), ('high', 8), ('much', 1)]
5 Most Repeated Adverbs In The Song: [('dumb', 6), ('so', 5), ('still', 4), ('just', 3), ('So', 1)]
5 Most Repeated 2-Word Phrases In The Song: [('young dumb', 29), ('dumb and', 12), ('and broke', 12), ('dumb young', 11), ('young young', 9)]
"""

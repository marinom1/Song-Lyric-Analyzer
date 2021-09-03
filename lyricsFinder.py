import json
import re
# from collections import Counter
from functionDefinitions import *

def main():
    # badSongIndices is list of song indices to NOT analyze

    khalidBadSongIndices = []

    counts = Counter()

    with open('Lyrics_Khalid_all.json') as json_file: data = json.load(json_file)

    print(find_total_unqiue_words_in_song(data , 0))
    print(find_total_words_in_song(data, 0))
    x = find_uniqueness_percent_of_song(data, 6)
    print(x)


main()

import json
import re
# from collections import Counter
from functionDefinitions import *

def main():
    # badSongIndices is list of song indices to NOT analyze

    khalidBadSongIndices = []

    counts = Counter()

    with open('Lyrics_Khalid_all.json') as json_file: data = json.load(json_file)

    printGoodSongsFromJSON(data, khalidBadSongIndices)
    getListOfSongsWithKeywordByArtist(data, 'life', khalidBadSongIndices, 'Khalid')


main()

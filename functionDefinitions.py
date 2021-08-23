import json
import os
from collections import Counter
import re


# Print Functions
def print_all_songs_from_json(data):
    """Prints all songs from the JSON

        Parameters
        -------
        data : json
            the json where the Genius data is stored in

        Returns
        -------
        listOfSongs : list
            list of all songs in data
    """
    list_of_songs = []
    for i in range(len(data['songs'])):
        print(i, data['songs'][i]['title'])
        list_of_songs.append(data['songs'][i]['title'].replace('\u200b', ''))
    return list_of_songs


def print_bad_songs_from_json(data, bad_song_indices):
    if not bad_song_indices: #if list is empty
        print("No bad song indices")
        return []
    if not is_valid_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them")
        return []
    list_of_songs = []
    for i in range(len(data['songs'])):
        if i not in bad_song_indices: # if song is good, don't print or store song in list
            continue
        list_of_songs.append(data['songs'][i]['title'])
        print(i, data['songs'][i]['title'])

    return list_of_songs


def print_good_songs_from_json(data, bad_song_indices):
    """Prints all songs that are not on the bad_song_indices list. Returns list of song names that are good songs"""
    totalGoodSongs = 0
    list_of_good_songs = []
    for i in range(len(data['songs'])):
        if i in bad_song_indices:
            continue
        print(i, data['songs'][i]['title'])
        totalGoodSongs = totalGoodSongs + 1
        list_of_good_songs.append(data['songs'][i]['title'])
    print("There are", totalGoodSongs, "good songs")
    return list_of_good_songs

# Helper Functions

def remove_punctuation(string):
    """Removes punctuation from a string

        Parameters
        -------
        string : str
            the string that needs punctuation removed from

        Returns
        -------
        string
            the string without punctuation
    """
    #punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    punc = '''!()-[]'{};:"\,<>./?@#$%^&*_~''' #Uncomment this to remove apostrophes as well
    for ele in string:
        if ele in punc:
            string = string.replace(ele, "")
    return string


def remove_headers_from_lyrics(lyrics):
    """Gets lyrics without the header tags, returns string"""
    indexPointer = 0
    while (13 == 13):
        startOfHeader = lyrics.find('[', indexPointer, len(lyrics))
        endOfHeader = lyrics.find(']', startOfHeader, len(lyrics))
        headerToRemove = lyrics[startOfHeader:endOfHeader + 1]
        lyrics = lyrics.replace(headerToRemove, '')
        if '[' not in lyrics:  # if no more headers to remove
            return lyrics

def get_only_artist_lyrics_in_song(data, song_index, artist_name):
    """Will go through a song and get only the lyrics said by the artist, returns string"""
    lyrics_only_from_artist = ''
    index_pointer = 0
    start_of_verse = 0
    end_of_verse = 1
    original_lyrics = data['songs'][song_index]['lyrics']
    # print("lyrics here is:",lyrics,"from song:",data['songs'][song_index]['title'])
    if ': ' + artist_name not in original_lyrics:  # If there are no other features on the song, headers will not say artist name
        if artist_name == data['songs'][song_index]['artist']:  # If artist name does not match Genius song owner, return error because user inputted an invalid artist name
            print(artist_name == data['songs'][song_index]['artist'])
            while ('[' in original_lyrics): # While lyrics still have headers in them
                start_of_header = original_lyrics.find('[', index_pointer, len(original_lyrics))
                end_of_header = original_lyrics.find(']', start_of_header, len(original_lyrics))
                header_to_remove = original_lyrics[start_of_header:end_of_header + 1]
                original_lyrics = original_lyrics.replace(header_to_remove, '')
                # print(lyrics)
                if '[' not in original_lyrics:  # if no more headers to remove
                    lyrics_only_from_artist = original_lyrics

        else:
            if (song_index < 0):
                print("Invalid song_index")
            else:
                print("Invalid artist name inputted by user")

    else:  # The song has 1 or more features
        while ': ' + artist_name in original_lyrics[index_pointer:len(original_lyrics)]:
            start_of_verse = original_lyrics.find((': ' + artist_name), index_pointer, len(original_lyrics)) + len(
                artist_name) + 4  # logic to skip the header and get right to lyrics
            end_of_verse = original_lyrics.find('\n\n', start_of_verse, len(original_lyrics))
            if end_of_verse == -1:  # If verse is last in the whole song, \n\n wont be found
                end_of_verse = len(original_lyrics)
            verse = original_lyrics[start_of_verse:end_of_verse]
            index_pointer = end_of_verse
            lyrics_only_from_artist = lyrics_only_from_artist + '\n' + verse

    return lyrics_only_from_artist

def is_valid_list(data, list_of_indices):
    if not all(isinstance(x, int) for x in list_of_indices): # if bad_song_indices has invalid value(s) e.g string, double
        print("Invalid song indices list input")
        return False
    # Check if indices are in valid range
    max_index = len(data['songs']) - 1
    for index in list_of_indices:
        if index < 0 or index > max_index:
            return False
    return True

def find_total_words_in_song(data, song_index):
    """Will count the number of words in a song, does not include headers

        Parameters
        -------
        data : json
            json with song info
        song_index : int
            index of song to check from json
        Returns
        -------
        total_word_count
            an int with how many total words are in the song
        """
    total_word_count = 0
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    total_word_count = len(lyrics.split())
    return total_word_count

def find_total_unqiue_words_in_song(data, song_index):
    """Will count the number of words in a song, does not include headers

        Parameters
        -------
        data : json
            json with song info
        song_index : int
            index of song to check from json
        Returns
        -------
        total_unique_word_count
            an int with how many total unqiue words are in the song
        """
    total_unique_word_count = 0
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    total_word_count = len(lyrics.split())
    return total_unique_word_count

# Write to CSV functions
def write_counter_to_csv(counter, outputFileName):
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')
    fp.write('Word|Frequency\n')
    for word, count in counter.most_common():
        fp.write('{}|{}\n'.format(word, count))

    fp.close()


def write_dict_to_csv(dict, outputFileName):
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')
    fp.write('Word|Frequency\n')
    for word, count in dict.items():
        fp.write('{}|{}\n'.format(word, count))
    fp.close()
    print("Finished writing dict to", outputFileName)


# Find Frequency of keyword in one or all songs
def find_keyword_count_in_song(data, keyword, songIndex):
    """Will check one song to see how many times the keyword occurs

        Parameters
        -------
        data : json
            json with song info
        keyword : str
            keyword to check in each song
        songIndex : int
            index of song to check from json
        Returns
        -------
        keywordCount
            an int with how often the keyword appears in the song
        """
    keywordCount = 0
    keyword = keyword.lower()
    lyrics = data['songs'][songIndex]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    songTitle = data['songs'][songIndex]['title']
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.replace('\u200b', '')  # catch weird bug where \u200b was showing up in some keywords
        lyrics = lyrics.split()
        # print(song_index, "Currently looking at: ", data['songs'][song_index]['title'])
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keywordCount = keywordCount + 1
        print("The number of times \"" + keyword + "\" is said in", songTitle, " is: ", keywordCount)
    return keywordCount


def find_keyword_count_in_all_songs(data, keyword, badSongIndices):
    """Will go through the entire list of songs (in data) and count how many times the keyword appears in total"""
    keyword = keyword.lower()
    keywordCount = 0
    for i in range(len(data['songs'])):  # Loop through every song in data
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        keywordCount = keywordCount + find_keyword_count_in_song(data, keyword, i)
    print("The total number of times", keyword, "is said in every song is: ", keywordCount, "\n")
    return keywordCount


def find_keyword_count_in_song_by_artist(data, keyword, songIndex, artistName):
    """Will check one song to see how many times the keyword is said by artist

        Parameters
        -------
        data : json
            json with song info
        keyword : str
            keyword to check in each song
        songIndex : int
            index of song to check from json
        artistName : str
            name of artist to only check lyrics from

        Returns
        -------
        keywordCount
            an int with how often the keyword appears in the artist's lyrics
        """

    keywordCount = 0
    keyword = keyword.lower()
    lyrics = get_only_artist_lyrics_in_song(data, songIndex, artistName)
    songTitle = data['songs'][songIndex]['title']
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        # print(song_index, "Currently looking at: ", data['songs'][song_index]['title'])
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keywordCount = keywordCount + 1
        print("The number of times \"" + keyword + "\" is said in", songTitle, "by", artistName, "is:", keywordCount)
    return keywordCount


def find_keyword_count_in_all_songs_by_artist(data, keyword, bad_song_indices, artist_name):
    """Will check all songs to see how many times keyword was said by artist in total"""
    total_count = 0

    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in bad_song_indices:
            continue
        current_count = find_keyword_count_in_song_by_artist(data, keyword, i, artist_name)
        total_count = total_count + current_count
    print("The number of times", keyword, "is said by", artist_name, "in all songs is:", total_count)
    return total_count


# Find Frequencies of keywords in one or all songs
def find_keyword_counts_in_song(data, list_of_keywords, song_index):
    """Takes a list of keywords and finds counts for every keyword that's in the song
    Parameters
        -------
        data : json
            json with song info
        list_of_keywords : list
            list of keywords to count for individually
        song_index : int
            index of song to check from json

        Returns
        -------
        list_of_keyword_counts : list
            a list of tuples where first value is the keyword, second value is int of occurrences
    """
    list_of_keyword_counts = []
    for keyword in list_of_keywords:  # Loop through all the keywords to count
        current_keyword = keyword
        list_of_keyword_counts.append((current_keyword, find_keyword_count_in_song(data, keyword, song_index)))
    print(list_of_keyword_counts)
    return list_of_keyword_counts


def find_keyword_counts_in_all_songs(data, list_of_keywords, bad_song_indices):
    """Takes a list of keywords and finds counts for every keyword in every song
    Parameters
        -------
        data : json
            json with song info
        list_of_keywords : list
            list of keywords to count for individually
        bad_song_indices : list
            list of song indices to ignore in the counts

        Returns
        -------
        list_of_keyword_counts : list
            a list of tuples where first value is the keyword, second value is int of occurrences
    """
    list_of_keyword_counts = []

    for i in range(len(list_of_keywords)):  # Loop through all the keywords to count
        current_cumulative_count = 0
        for j in range(len(data['songs'])):  # Loop through every song in data
            if j in bad_song_indices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
                continue
            current_cumulative_count = current_cumulative_count + find_keyword_count_in_song(data, list_of_keywords[i], j)
        list_of_keyword_counts.append((list_of_keywords[i], current_cumulative_count))

    print(list_of_keyword_counts)
    return list_of_keyword_counts


def find_noun_counts_in_song(data, song_index):
    """"Find counts for every noun in the song

        Parameters
        -------
        data : json
            the json where the Genius data is stored in

        song_index : int
            the song index of the song we want to find noun counts for

        Returns
        -------
        counts : Counter
            Counter object of all nouns in the song and their counts
    """

    counts = Counter()
    from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    counts = findAllWordCountsInSong(data, song_index, counts)
    for word in list(counts):  # filter out the words that arent nouns
        if word not in nouns:
            del counts[word]
    print(counts)
    return counts


def find_noun_counts_in_all_songs(data, bad_song_indices):
    """Find counts for every noun in all songs

        Parameters
        -------
        data : json
            the json where the Genius data is stored in

        bad_song_indices : list
            list of song indices for songs we don't want to count for

        Returns
        -------
        cumulative_counts : Counter
            Counter object of all nouns in every song and their cumulative counts
    """

    cumulative_counts = Counter()
    from nltk.corpus import wordnet as wn  # this takes some time, so only load it if we use this function
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    counts = Counter()
    cumulative_counts = findAllWordCountsInAllSongs(data, counts, bad_song_indices)

    for word in list(cumulative_counts):
        if word not in nouns:
            del cumulative_counts[word]
    print(cumulative_counts)
    return cumulative_counts



def find_keyword_counts_and_compact_variants_in_all_songs(data, counts, list_of_list_of_words, bad_song_indices):
    """Returns a dictionary with the totals for each root word in list_of_list_of_words
    For example, if I want to find how many times "cat" is referenced, along with
    cat synonyms, cat plural, cat slang, etc. we give the function a list of lists of words
    that is [['cat','cats','feline','felines']] and it will return a dictionary with one
    element in it, {'cat': 46} even if the exact word "cat" appeared 37 times, it counted
    46 because 'cats' appeared 3 times, 'feline' appeared 2 times, and 'felines' appeared
    4 times - for a total of 46 times.

    Parameters
    ----------
    data : json
        The json holding all the info
    counts : Counter
        Counter Object that
    list_of_list_of_words : list
        list of lists where the first entry in a list is the root word, and everything after are the word variances
    bad_song_indices : list
        list of song indices we don't want to work with

    Returns
    -------
    dict_of_totals
        dictionary of each root word and their frequencies
    """
    dict_of_totals = {}
    for i in range(len(list_of_list_of_words)):
        all_count = findAllWordCountsInAllSongs(data, counts, bad_song_indices)
        print("All the words are: ", all_count)
        custom_count = customWhiteListCountObject(all_count, list_of_list_of_words[i])
        print("The words after white-listing are: ", custom_count)
        total = 0
        for key in custom_count.keys():  # Loop to add up all the variants together to find total of root word
            # print("Key here is: ",custom_count.get(key))
            total = total + custom_count.get(key)
        print("\"" + list_of_list_of_words[i][0] + "\" and all its variants add up to: ", total, "\n")
        dict_of_totals[list_of_list_of_words[i][0]] = total

    print("The final words and their variants add up to: ", dict_of_totals)
    return dict_of_totals


def find_keyword_counts_and_compact_variants_in_all_songs_by_artist(data, counts, list_of_list_of_words, bad_song_indices, artist_name):
    """Returns a dictionary with the totals for each root word in list_of_list_of_words
        For example, if I want to find how many times "cat" is referenced, along with
        cat synonyms, cat plural, cat slang, etc. we give the function a list of lists of words
        that is [['cat','cats','feline','felines']] and it will return a dictionary with one
        element in it, {'cat': 46} even if the exact word "cat" appeared 37 times, it counted
        46 because 'cats' appeared 3 times, 'feline' appeared 2 times, and 'felines' appeared
        4 times - for a total of 46 times.

        Parameters
        ----------
        data : json
            The json holding all the info
        counts : Counter
            Counter Object that
        list_of_list_of_words : list
            list of lists where the first entry in a list is the root word, and everything after are the word variances
        bad_song_indices : list
            list of song indices we don't want to work with

        Returns
        -------
        dict_of_totals
            dictionary of each root word and their frequencies
        """
    dict_of_totals = {}
    for i in range(len(list_of_list_of_words)):
        all_count = findAllWordCountsInAllSongsByArtist(data, counts, bad_song_indices, artist_name)
        print("All the words are: ", all_count)
        custom_count = customWhiteListCountObject(all_count, list_of_list_of_words[i])
        print("The words after white-listing are: ", custom_count)
        total = 0
        for key in custom_count.keys():  # Loop to add up all the variants together to find total of root word
            # print("Key here is: ",custom_count.get(key))
            total = total + custom_count.get(key)
        print("\"" + list_of_list_of_words[i][0] + "\" and all its variants add up to: ", total, "\n")
        dict_of_totals[list_of_list_of_words[i][0]] = total

    print("The final words and their variants add up to: ", dict_of_totals)
    return dict_of_totals

# Find Frequency(s) of a phrase in one or more songs
def find_phrase_count_in_song(data, phrase, songIndex):
    """Find phrase frequency in a song - will include ad libs (lyrics in parenthesis)"""
    phrase_count = 0
    phrase = phrase.lower()
    string_of_words = data['songs'][songIndex]['lyrics']
    song_title = data['songs'][songIndex]['title']
    if string_of_words is not None:
        string_of_words = string_of_words.lower()
        string_of_words = remove_headers_from_lyrics(string_of_words)
        string_of_words = remove_punctuation(string_of_words)
        string_of_words = string_of_words.replace('\u2005', ' ') # This catches weird bug I randomly found where spaces werent actually spaces...
        #print("lyrics should be good to go here:", string_of_words)
        print(repr(string_of_words))
        print(songIndex, "Currently looking at: ", data['songs'][songIndex]['title'])
        list_of_matches = re.findall(r'\b' + phrase + r'\b', string_of_words)
        # print(list_of_matches)
        phrase_count = len(list_of_matches)
    print("The number of times \"" + phrase + "\" is said in \"" + song_title + "\" is: ", phrase_count)
    return phrase_count


def find_phrase_count_in_all_songs(data, phrase, bad_song_indices):
    """Find phrase in all songs"""
    print("Finding \"" + phrase + "\" in All Songs...")
    phrase_count = 0
    phrase = phrase.lower()
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in bad_song_indices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        list_of_words = data['songs'][i]['lyrics']
        if list_of_words is not None:
            list_of_words = list_of_words.lower()
            list_of_words = remove_punctuation(list_of_words)
            # print(i, "Currently looking at: ", data['songs'][i]['title'])
            phrase_count = phrase_count + find_phrase_count_in_song(data, phrase, i)
    print("The total number of times", phrase, "is said is: ", phrase_count, "\n")
    return phrase_count


def find_phrase_counts_in_song(data, list_of_phrases, song_index):
    """Takes a list of phrases and finds counts for every phase in the list"""
    list_of_phrase_counts = []
    for i in range(len(list_of_phrases)):
        current_phrase = list_of_phrases[i]

        list_of_phrase_counts.append((current_phrase, find_phrase_count_in_song(data, list_of_phrases[i], song_index)))
        print(list_of_phrase_counts)

    print(list_of_phrase_counts)
    return list_of_phrase_counts

def find_phrase_count_in_song_by_artist(data, phrase, song_index, artist_name):
    """Find phrase frequency in a song by only the artist- will include ad libs (lyrics in parenthesis)"""
    phrase_count = 0
    phrase = phrase.lower()
    string_of_words = get_only_artist_lyrics_in_song(data, song_index, artist_name)
    print(string_of_words)
    song_title = data['songs'][song_index]['title']
    if string_of_words is not None:
        string_of_words = string_of_words.lower()
        string_of_words = remove_punctuation(string_of_words)
        print(song_index, "Currently looking at: ", data['songs'][song_index]['title'])
        list_of_matches = re.findall(r'\b' + phrase + r'\b', string_of_words)
        # print(list_of_matches)
        phrase_count = len(list_of_matches)
    print("The number of times \"" + phrase + "\" is said in \"" + song_title + "\" by", artist_name, " is: ",
          phrase_count)
    return phrase_count


# Find the Song Where a Keyword or Phrase is said the most
def find_song_where_keyword_is_said_the_most(data, keyword, bad_song_indices):
    highest_count = find_keyword_count_in_song(data, keyword, 0)
    title_of_highest_count = ''
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in bad_song_indices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        current_count = find_keyword_count_in_song(data, keyword, i)
        if current_count > highest_count:
            highest_count = current_count
            title_of_highest_count = data['songs'][i]['title']
        elif current_count == highest_count:
            print("todo")

    list_of_info = [highest_count, title_of_highest_count]
    print("The song with the most occurrences of", keyword, "is: ", title_of_highest_count, "with a count of:",
          highest_count, "occurrences.")

    return list_of_info


def find_song_where_phrase_is_said_the_most(data, phrase, bad_song_indices):
    highest_count = find_keyword_count_in_song(data, phrase, 0)
    title_of_highest_count = ''
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in bad_song_indices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        current_count = find_phrase_count_in_song(data, phrase, i)
        if current_count > highest_count:
            highest_count = current_count
            title_of_highest_count = data['songs'][i]['title']

    list_of_info = [highest_count, title_of_highest_count]
    print("The song with the most occurrences of", phrase, "is: ", title_of_highest_count, "with a count of:", highest_count,
          "occurrences.")
    return list_of_info


# Find All or Most Word Counts in specific song or every song
def findAllWordCountsInSong(data, songIndex, counts):
    """Counts how often every word occurs in a song

        Parameters
        -------
        data : json
            the json where the Genius data is stored in
        songIndex : int
            index of song in the json to look at
        counts : Counter
            Counter Object that will hold every word and how often it occurs

        Returns
        -------
        counts : list
            Counter Object of all words and their counts in the song

    """
    lyrics = data['songs'][songIndex]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        counts = counts + Counter(lyrics)
        # print(counts)
    return counts


def findAllWordCountsInAllSongs(data, cumulativeCounts, badSongIndices):
    """Counts how often every word occurs cumulatively in every song in data"""
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        cumulativeCounts = findAllWordCountsInSong(data, i, cumulativeCounts)
    #    print(i,"cumulativeCounts here is: ",cumulativeCounts)

    # print("The total counts are: ", cumulativeCounts)

    return cumulativeCounts


def findMostWordCountsInSong(data, songIndex, counts, wordsToOmit):
    """Counts how often every word occurs in a song minus the omitted words"""
    lyrics = data['songs'][songIndex]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        counts = counts + Counter(lyrics)

    for word in wordsToOmit:
        if word in counts:
            del counts[word]
    return counts


def findMostWordCountsInAllSongs(data, cumulativeCounts, badSongIndices, wordsToOmit):
    """Counts how often every word occurs minus the omitted words cumulatively in every song in data"""
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        cumulativeCounts = findAllWordCountsInSong(data, i, cumulativeCounts)

    for word in wordsToOmit:
        if word in cumulativeCounts:
            del cumulativeCounts[word]
    return cumulativeCounts


def findAllWordCountsInSongByArtist(data, songIndex, counts, artistName):
    """"Counts the frequency of every word in the song only by the specified artist"""
    listOfEachLyric = get_only_artist_lyrics_in_song(data, songIndex, artistName)
    if listOfEachLyric is not None:
        listOfEachLyric = listOfEachLyric.lower()
        listOfEachLyric = remove_punctuation(listOfEachLyric)
        listOfEachLyric = listOfEachLyric.split()
        counts = counts + Counter(listOfEachLyric)
    return counts


def findAllWordCountsInAllSongsByArtist(data, cumulativeCounts, badSongIndices, artistName):
    """Counts how often every word occurs cumulatively in every song in data by only the artist specified"""
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:
            continue
        cumulativeCounts = findAllWordCountsInSongByArtist(data, i, cumulativeCounts, artistName)
    return cumulativeCounts


# Find list of songs containing the keyword or phrase
def getListOfSongsWithKeyword(data, keyword, badSongIndices):
    """Get list of songs that have at least 1 occurrence of the keyword"""
    listOfSongs = []
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:
            continue
        if find_keyword_count_in_song(data, keyword, i) > 0:
            listOfSongs.append(data['songs'][i]['title'])
    print("The list of", len(listOfSongs), "song(s) containing the word \"" + keyword + "\" are: ", listOfSongs)
    return listOfSongs


def getListOfSongsWithPhrase(data, phrase, badSongIndices):
    """Get list of songs that have at least 1 occurrence of the phrase"""
    listOfSongs = []
    phrase = phrase.lower()
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        lyrics = data['songs'][i]['lyrics']
        lyrics = remove_headers_from_lyrics(lyrics)
        songTitle = data['songs'][i]['title']
        if lyrics is not None:
            lyrics = lyrics.lower()
            lyrics = remove_punctuation(lyrics)
            lyrics = lyrics.replace('\u2005', ' ') #This catches weird bug I randomly found where spaces werent actually spaces...
            # print(i, "Currently looking at: ", data['songs'][i]['title'])
            listOfMatches = re.findall(r'\b' + phrase + r'\b', lyrics)
            # print(listOfMatches)
            phraseCount = len(listOfMatches)
            # print("The number of times \"" + phrase + "\" is said in \"" + songTitle + "\" is: ", phraseCount)
            if phraseCount > 0:
                listOfSongs.append(songTitle.replace('\u200b',
                                                     ''))  # the replace catches weird bug where \u200b was showing up in print(listOfSongs) entries

    print("The list of", len(listOfSongs), "songs containing the phrase \"" + phrase + "\" are: ", listOfSongs)
    return listOfSongs

def getListOfSongsWithoutPhrase(data, phrase, badSongIndices):
    listOfAllSongs = []
    listOfSongsWithPhrase = getListOfSongsWithPhrase(data, phrase, badSongIndices)
    listofSongsWithoutPhrase = []
    for i in range(len(data['songs'])):
        if i in badSongIndices:
            continue
        currentSongTitle = data['songs'][i]['title']
        currentSongTitle = currentSongTitle.replace('\u200b', '')
        listOfAllSongs.append(currentSongTitle)
    for i in range(len(listOfAllSongs)):
        if listOfAllSongs[i] in listOfSongsWithPhrase:
            continue
        else:
            listofSongsWithoutPhrase.append(listOfAllSongs[i])

    print("The list of",len(listofSongsWithoutPhrase), "songs without the phrase \""+phrase+"\" are:", listofSongsWithoutPhrase)
    return listofSongsWithoutPhrase

def getListOfSongsWithKeywordByArtist(data, keyword, badSongIndices, artistName):
    """Gets list of songs that have at least 1 occurrence of the keyword by the artist"""
    listOfSongs = []
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        lyrics = get_only_artist_lyrics_in_song(data, i, artistName)
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        if keyword in lyrics:
            listOfSongs.append(data['songs'][i]['title'].replace('\u200b', ''))
    print("The list of", len(listOfSongs), "song(s) containing the word \"" + keyword + "\" said by", artistName,
          "are: ", listOfSongs)

    return listOfSongs


def getListOfSongsWithPhraseByArtist(data, phrase, badSongIndices, artistName):
    """Gets list of songs that have at least 1 occurrence of the phrase by the artist"""
    listOfSongs = []
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        lyrics = get_only_artist_lyrics_in_song(data, i, artistName)
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        listOfMatches = re.findall(r'\b' + phrase + r'\b', lyrics)
        phraseCount = len(listOfMatches)
        if phraseCount > 0:
            listOfSongs.append(data['songs'][i]['title'].replace('\u200b', ''))
    print("The list of", len(listOfSongs), "song(s) containing the phrase \"" + phrase + "\" said by", artistName,
          "are: ", listOfSongs)

    return listOfSongs


# Filter Count Objects
def filter_count_object(counts, partOfSpeech):
    """Removes words that don't fall under the partOfSpeech from a Counter Object"""

    if (partOfSpeech == 'noun'):
        from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
        goodWords = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    elif (partOfSpeech == 'verb'):
        from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
        goodWords = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
    elif (partOfSpeech == 'adjective'):
        from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
        goodWords = {x.name().split('.', 1)[0] for x in wn.all_synsets('a')}
    else:
        print("Invalid part of speech input")
        return counts

    for word in list(counts):  # filter out the words that aren't in goodWords
        if word not in goodWords:
            del counts[word]

    return counts


def customBlackListCountObject(counts, blackList):
    """Removes words that are in the blackList from Counter Object"""
    for word in list(counts):  # filter out the words that aren't in goodWords
        if word in blackList:
            del counts[word]
    return counts


def customWhiteListCountObject(counts, whiteList):
    """Removes words that are not in the whiteList from Counter Object"""
    for word in list(counts):  # filter out the words that aren't in goodWords
        if word not in whiteList:
            del counts[word]
    return counts


def getNumberOfWordsInSong(data, songIndex):
    """Count how many words are in a song"""
    total = 0
    lyrics = data['songs'][songIndex]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = lyrics.split()
    total = len(lyrics)
    return total


def writeCounterToCustomCSV(counts, outputFileName):
    """Writes CSV in way that wordart.com accepts it as an import"""
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')

    for word, count in counts.most_common(20):
        fp.write('{};{}\n'.format(word, count))

    fp.close()

def findCommonTwoWordPhrasesInTwoSongs(data, songIndex1, songIndex2):
    """Get list of two word common phrases among both songs"""
    string1 = data['songs'][songIndex1]['lyrics'].lower()
    string1 = remove_headers_from_lyrics(string1)
    string1 = remove_punctuation(string1)
    string1 = string1.replace('\n', ' ')
    string2 = data['songs'][songIndex2]['lyrics'].lower()
    string2 = remove_headers_from_lyrics(string2)
    string2 = remove_punctuation(string2)
    string2 = string2.replace('\n', ' ')
    list1 = string1.split()
    list2 = string2.split()
    commonPhrases = set()

    for i in range(len(list1)-1): #Loop through each 2 word phrase in song 1
        firstPhrase = list1[i] + ' ' + list1[i+1]
        for j in range(len(list2)-1): #loop through each 2 word phrase in song 2
            secondPhrase = list2[j] + ' ' + list2[j+1]
            # print("First phrase: ", firstPhrase)
            # print("Second phrase: ", secondPhrase)
            if firstPhrase == secondPhrase:
                commonPhrases.add(firstPhrase)


    print("The common 2 word phrases from both songs are: ",commonPhrases)
    return commonPhrases

def findHowManySongsEachPhraseOccurs(data, badSongIndices):
    """Return dictionary with key as two word phrase and value is how many songs that phrase occurs in"""
    print("5")

def getTwoWordPhrasesInSong(data, songIndex):
    """Return list of all two word phrases from the song. No duplicates"""
    lyrics = data['songs'][songIndex]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = lyrics.lower()
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.split()
    listOfPhrases = []
    for i in range(len(lyrics)-1):
        phrase = lyrics[i] + " " + lyrics[i+1]
        listOfPhrases.append(phrase)

    listOfPhrasesWithoutDuplicates = []
    for i in listOfPhrases:
        if i not in listOfPhrasesWithoutDuplicates:
            listOfPhrasesWithoutDuplicates.append(i)

    return listOfPhrasesWithoutDuplicates

def getListOfMostCommonTwoWordPhrasesInAllSongs(data, badSongIndices):
    """Returns list of every song's unique two word phrases. Duplicates mean the phrase is in more than 1 song"""
    cumulativeListOfPhrases = []
    songCount = 0
    for i in range(len(data['songs'])):
        if i not in badSongIndices:
            initialSong = i
            break
    cumulativeListOfPhrases = getTwoWordPhrasesInSong(data, initialSong)  # Initial Cumulative list is just set to first song

    for i in range(initialSong+1,len(data['songs'])):  # Loop through all the songs
        if i not in badSongIndices:
            songCount = songCount + 1
            print("i here is:", i)
            currentSong = getTwoWordPhrasesInSong(data, i)
            cumulativeListOfPhrases.extend(currentSong)
    z = Counter(cumulativeListOfPhrases)
    print("Checked ", songCount, "songs")
    return z

    return cumulativeListOfPhrases


def get_list_of_artists_in_song(data, song_index):
    """Returns a list of all the artists on the song"""
    # First add the name of the JSON artist
    list_of_artists = []
    list_of_artists.append(data['name'])
    #Now add the song owner if not the same as JSON artist
    current_artist = data["songs"][song_index]["primary_artist"]["name"]
    if current_artist not in list_of_artists:
        list_of_artists.append(current_artist)

    # Now Loop through the list of featured artists and add to list_of_artists
    for i in range(len(data["songs"][song_index]["featured_artists"])):
        current_artist = data["songs"][song_index]["featured_artists"][i]["name"]
        if current_artist not in list_of_artists:
            list_of_artists.append(current_artist)
    list_of_artists.sort()
    return list_of_artists


def get_list_of_artists_in_JSON(data, bad_song_indices):
    """Loops through all the songs in the json, then return a alphabeticalized list with all the different artists that
    appear in the JSON"""
    # First add the name of the JSON artist
    list_of_artists = []
    list_of_artists.append(data['name'])
    # Now Loop through all the songs and add name to list if it wasn't added before
    # First loop to check for primary artist of all songs
    for i in range(len(data["songs"])):
        if i not in bad_song_indices:
            current_artist = data["songs"][i]["primary_artist"]["name"]
            if current_artist not in list_of_artists:
                list_of_artists.append(current_artist)
    # Next loop to check for other featured artists on the same song
    for i in range(len(data["songs"])):
        if i not in bad_song_indices:
            for j in range (len(data["songs"][i]["featured_artists"])):
                current_artist = data["songs"][i]["featured_artists"][j]["name"]
                if current_artist not in list_of_artists:
                    list_of_artists.append(current_artist)
    list_of_artists.sort()
    return list_of_artists

# GUI Functions
def load_existing_presets():
    """First, this function will ensure that the file presets.json exists. If it doesn't, then we create it.
    Then, this function checks if there are already existing presets. If there are, we load them into program.
    If there are no existing presets, then make the boolean existing_presets False
    Returns
    -------
    there_are_existing_presets : bool
        boolean that tells us if there are existing presets already in presets.json
    loaded_presets : json
        existing data from presets.json if there are existing presets, empty dict if there are none
    """

    # Check if profiles.json exists first
    if os.path.isfile("presets.json"):
        print("Found presets.json - Loading presets Now")
    else:
        print("presets.json doesn't exist - Creating presets.json")
        f = open("presets.json", "w")
        f.write("")  # dont think this is needed anymore

    if os.stat("presets.json").st_size == 0:  # if presets.json is empty (A.K.A no existing profiles)
        there_are_existing_presets = False
    else:
        there_are_existing_presets = True

    if (there_are_existing_presets):
        with open('presets.json') as json_file:
            loaded_presets = json.load(json_file)

    else:  # No presets made previously
        loaded_presets = {}

    return there_are_existing_presets, loaded_presets
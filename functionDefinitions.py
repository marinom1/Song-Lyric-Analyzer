import json
import os
import sys
from collections import Counter
import re

# Print Functions
def print_all_songs_from_json(data):
    """
    Prints all songs from the JSON generated from the LyricsGenius Python client search_artist function

    Parameters
    -------
    data : json
        the json where the Genius data is stored in

    Returns
    -------
    list
        list of all songs in data
    """
    list_of_songs = []
    for i in range(len(data['songs'])):
        print(i, data['songs'][i]['title'])
        list_of_songs.append(data['songs'][i]['title'].replace('\u200b', ''))
    return list_of_songs


def print_bad_songs_from_json(data, bad_song_indices):
    """
    Prints all the song titles whose indices appear in bad_song_indices. If there are invalid elements in
    bad_song_indices, then prints there were invalid values and shows a list of what the invalid elements were

    Parameters
    -------
    data : json
        the json where the Genius data is stored in
    bad_song_indices : list
        list of song indices to print their titles

    Returns
    -------
    list
        list of songs whose indices appeared in bad_song_indices or empty list if errors encountered
    """
    if not bad_song_indices: #if list is empty
        print("No bad song indices")
        return []
    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return []
    list_of_songs = []

    # All values are valid at this point, now remove any duplicate values
    if not len(set(bad_song_indices)) == len(bad_song_indices):
        bad_song_indices = remove_duplicate_valid_indices(bad_song_indices)

    for index in bad_song_indices:
        list_of_songs.append(data['songs'][index]['title'].replace('\u200b', ''))
        print(index, data['songs'][index]['title'])

    return list_of_songs


def print_good_songs_from_json(data, bad_song_indices):
    """
    Prints all songs that are not on the bad_song_indices list. Returns list of song names that are good songs

    Parameters
    -------
    data : json
        the json where the Genius data is stored in
    bad_song_indices : list
        list of song indices to print their titles

    Returns
    -------
    list
        list of songs whose indices do not appear in bad_song_indices, or empty list if errors encountered
    """

    if not bad_song_indices: #if list is empty
        print("No bad song indices")
    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return []

    total_good_songs = 0
    list_of_good_songs = []
    for i in range(len(data['songs'])):
        if i in set(bad_song_indices):
            continue
        print(i, data['songs'][i]['title'])
        total_good_songs = total_good_songs + 1
        list_of_good_songs.append(data['songs'][i]['title'].replace('\u200b', ''))
    print("There are", total_good_songs, "good songs")
    return list_of_good_songs

# Helper Functions

def remove_duplicate_valid_indices(list_of_song_indices):
    """
    Removes duplicate valid indices from list_of_song_indices. Order is kept from the first appearance of a repeated
    value.

    Parameters
    -------
    list_of_song_indices : list
        the list that needs duplicate values removed from

    Returns
    -------
    list
        the list with duplicates removed and order maintained
    """
    seen = set()
    seen_add = seen.add
    return [x for x in list_of_song_indices if not (x in seen or seen_add(x))]

def remove_punctuation(string):
    """
    Removes punctuation from a string

    Parameters
    -------
    string : str
        the string that needs punctuation removed from

    Returns
    -------
    string
        the string without punctuation
    """
    punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    #punc = '''!()-[]'{};:"\,<>./?@#$%^&*_~''' #Uncomment this to remove apostrophes as well
    for ele in string:
        if ele in set(punc):
            string = string.replace(ele, "")
    return string

def remove_unneeded_headers_and_footers(lyrics):
    """
        Gets lyrics without the unnessarry "[Song Name] Lyrics" at the start and the [number]Embed at the end.
        This has only started popping up in retrieved lyrics recently and hopefully will be fixed by LyricsGenius
        soon.

        Parameters
        -------
        lyrics : str
            the string that needs headers removed from

        Returns
        -------
        string
            the string without the unnecessary headers and footers
        """

    # Remove header first
    if " Lyrics[" in lyrics:
        start_of_header = 0
        end_of_header = lyrics.find(' Lyrics[', start_of_header, len(lyrics))
        header_to_remove = lyrics[start_of_header:end_of_header + 7]
        lyrics = lyrics.replace(header_to_remove, '')

        # Now remove footer
        start_of_footer = len(lyrics) - 6
        end_of_footer = len(lyrics)
        char_is_digit = True
        while char_is_digit:
            current_char = lyrics[start_of_footer]
            if current_char.isdigit():
                char_is_digit = True
                start_of_footer = start_of_footer - 1
            else:
                char_is_digit = False
                start_of_footer = start_of_footer + 1
        footer_to_remove = lyrics[start_of_footer:end_of_footer]
        lyrics = lyrics.replace(footer_to_remove, '')
    return lyrics

def remove_headers_from_lyrics(lyrics):
    """
    Gets lyrics without the header tags, returns the lyrics with the headers removed
    Example headers: [Verse 1: Khalid] , [Chorus] , [Intro]

    Parameters
    -------
    lyrics : str
        the string that needs headers removed from

    Returns
    -------
    string
        the string without the headers
    """
    lyrics = remove_unneeded_headers_and_footers(lyrics)
    index_pointer = 0
    while '[' in lyrics:
        start_of_header = lyrics.find('[', index_pointer, len(lyrics))
        end_of_header = lyrics.find(']', start_of_header, len(lyrics))
        header_to_remove = lyrics[start_of_header:end_of_header + 1]
        lyrics = lyrics.replace(header_to_remove, '')
    return lyrics

def get_only_artist_lyrics_in_song(data, song_index, artist_name):
    """
    Will go through a song and get only the lyrics said by the artist. Headers are removed.

    Parameters
    -------
    data : json
        the json where the Genius data is stored in
    song_index : int
        index of the song to retrieve lyrics for
    artist_name : str
        string of the artist's name to only get lyrics for

    Returns
    -------
    string
        the string of lyrics only from the specified artist
    """
    lyrics_only_from_artist = ''
    index_pointer = 0
    start_of_verse = 0
    end_of_verse = 1
    original_lyrics = data['songs'][song_index]['lyrics']
    # print("lyrics here is:",lyrics,"from song:",data['songs'][song_index]['title'])
    if ': ' + artist_name not in original_lyrics:  # If there are no other features on the song, headers will not say artist name
        if artist_name == data['songs'][song_index]['artist']:  # If artist name does not match Genius song owner, return error because user inputted an invalid artist name
            #print(artist_name == data['songs'][song_index]['artist'])
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
                pass
            else:
                #print("Invalid artist name inputted by user")
                pass

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

def is_valid_indices_list(data, list_of_indices):
    """
    Checks if a list of indices contains only valid index values. A list is valid only if it contains indices
    between 0 and the number of songs in data - 1. Negative numbers, indices out of range, strings, lists, etc are all
    invalud values to be inside of list_of_indices and will make function return false.

    Parameters
    -------
    data : json
        the json where the Genius data is stored in
    list_of_indices : list
        the list of indices to check
    Returns
    -------
    bool
        True if list contains valid indices (or is empty), false if list contains invalid value(s)
    """
    if not all(isinstance(x, int) for x in list_of_indices): # if bad_song_indices has invalid value(s) e.g string, double
        return False
    # Check if indices are in valid range
    max_index = len(data['songs']) - 1
    for index in list_of_indices:
        if index < 0 or index > max_index:
            return False
    return True

def find_total_words_in_song(data, song_index):
    """
    Will count the number of words in a song, does not include headers

    Parameters
    -------
    data : json
        json with song info
    song_index : int
        index of song to check from json
    Returns
    -------
    int
        an int with how many total words are in the song
    """
    total_word_count = 0
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.lower()
    total_word_count = len(lyrics.split())
    return total_word_count

def find_total_words_in_song_by_artist(data, song_index, artist_name):
    """
    Will count the number of words in a song by artist, does not include headers

    Parameters
    -------
    data : json
        json with song info
    song_index : int
        index of song to check from json
    artist_name : str
        string of the artist's name to only count words for

    Returns
    -------
    int
        an int with how many total words are in the song
    """
    total_word_count = 0
    lyrics = get_only_artist_lyrics_in_song(data, song_index, artist_name)
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.lower()
    total_word_count = len(lyrics.split())
    return total_word_count

def find_total_unique_words_in_song(data, song_index):
    """
    Will count the number of unique words in a song, does not include headers

    Parameters
    -------
    data : json
        json with song info
    song_index : int
        index of song to check from json

    Returns
    -------
    int
        an int with how many total unqiue words are in the song
    """
    total_unique_word_count = 0
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.lower()
    list_of_words = lyrics.split()
    total_unique_word_count = len(set(list_of_words))
    return total_unique_word_count

def find_total_unique_words_in_song_by_artist(data, song_index, artist_name):
    """
    Will count the number of unique words in a song by an artist, does not include headers

    Parameters
    -------
    data : json
        json with song info
    song_index : int
        index of song to check from json
    artist_name : str
        string of the artist's name to only get lyrics for

    Returns
    -------
    int
        an int with how many total unqiue words are in the song
    """
    total_unique_word_count = 0
    lyrics = get_only_artist_lyrics_in_song(data, song_index, artist_name)
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.lower()
    list_of_words = lyrics.split()
    total_unique_word_count = len(set(list_of_words))
    return total_unique_word_count

def find_uniqueness_percent_of_song(data, song_index):
    """
    Returns the uniqueness value of a specified song. The uniqueness percent of a song tells us how much of a song's lyrics are unique. The formula for calculating
    this value is unique_words/total_words. Round sto 4 decimal places

    Parameters
    -------
    data : json
        json with song info
    song_index : int
        index of song to check from json

    Returns
    -------
    float
        a float showing the percent of unique words in the song's lyrics
    """
    uniqueness_percent = 0
    uniqueness_percent = find_total_unique_words_in_song(data, song_index) / find_total_words_in_song(data, song_index) * 100

    return round(uniqueness_percent, 4)

def find_uniqueness_percent_of_song_by_artist(data, song_index, artist_name):
    """
    Returns the uniqueness value of a specified song by the specified artist. The uniqueness percent of a song tells us how much of a song's lyrics are unique. The formula for calculating
    this value is unique_words/total_words.

    Parameters
    ----------
    data : json
        json with song info
    song_index : int
        index of song to check from json
    artist_name : str
        string of the artist's name to only get lyrics for

    Returns
    -------
    float
        a float showing the percent of unique words in the song's lyrics said by the specified artist
    """
    uniqueness_percent = find_total_unique_words_in_song_by_artist(data, song_index, artist_name) / find_total_words_in_song_by_artist(data,song_index, artist_name) * 100
    return round(uniqueness_percent, 4)

def get_spacy_nlp_object(text):
    """ TODO
    Uses spacy to process a string. The processed object contains information including tokenized componenets, part of
    speech tagging, etc. Returns the spacy object
    Parameters
    ----------
    text

    Returns
    -------

    """
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return doc


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

def writeCounterToCustomCSV(counts, outputFileName):
    """Writes CSV in way that wordart.com accepts it as an import"""
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')

    for word, count in counts.most_common(20):
        fp.write('{};{}\n'.format(word, count))

    fp.close()

# Find Frequency of keyword in one or all songs
def find_keyword_count_in_song(data, keyword, song_index):
    """
    Will check one song to see how many times the keyword occursT

    Parameters
    -------
    data : json
        json with song info
    keyword : str
        keyword to check in each song
    song_index : int
        index of song to check from json

    Returns
    -------
    int
        an int with how often the keyword appears in the song
    """
    keywordCount = 0
    keyword = keyword.lower()
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    song_title = data['songs'][song_index]['title']
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.replace('\u200b', '')  # catch weird bug where \u200b was showing up in some keywords
        lyrics = lyrics.split()
        # print(song_index, "Currently looking at: ", data['songs'][song_index]['title'])
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keywordCount = keywordCount + 1
        # print("The number of times \"" + keyword + "\" is said in", song_title, " is: ", keywordCount)
    return keywordCount


def find_keyword_count_in_all_songs(data, keyword, bad_song_indices):
    """
    Will go through the entire list of songs (in data) and count how many times the keyword appears in total

    Parameters
    -------
    data : json
        json with song info
    keyword : str
        the word to count in all the songs in data
    bad_song_indices : list
        list of song indices to print their titles

    Returns
    -------
    int
        returns an int with the number of occurences the keyword appears in all songs
    """

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return 0

    keyword = keyword.lower()
    keyword_count = 0
    for i in range(len(data['songs'])):  # Loop through every song in data
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        keyword_count = keyword_count + find_keyword_count_in_song(data, keyword, i)
    # print("The total number of times", keyword, "is said in every song is: ", keyword_count, "\n")
    return keyword_count


def find_keyword_count_in_song_by_artist(data, keyword, song_index, artist_name):
    """
    Will check one song to see how many times the keyword is said by artist

    Parameters
    -------
    data : json
        json with song info
    keyword : str
        keyword to check in each song
    song_index : int
        index of song to check from json
    artist_name : str
        name of artist to only check lyrics from

    Returns
    -------
    int
        an int with how often the keyword appears in the artist's lyrics
    """

    keyword_count = 0
    keyword = keyword.lower()
    lyrics = get_only_artist_lyrics_in_song(data, song_index, artist_name)
    song_title = data['songs'][song_index]['title']
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        # print(song_index, "Currently looking at: ", data['songs'][song_index]['title'])
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keyword_count = keyword_count + 1
        # print("The number of times \"" + keyword + "\" is said in", song_title, "by", artist_name, "is:", keyword_count)
    return keyword_count


def find_keyword_count_in_all_songs_by_artist(data, keyword, bad_song_indices, artist_name):
    """
    Will check all songs to see how many times keyword was said by artist in total

    Parameters
    -------
    data : json
        json with song info
    keyword : str
        keyword to check in each song
    bad_song_indices : int
        list of song indices to print their titles
    artist_name : str
        name of artist to only check lyrics from

    Returns
    -------
    int
        return value description here
    """

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return 0

    total_count = 0
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in set(bad_song_indices):
            continue
        current_count = find_keyword_count_in_song_by_artist(data, keyword, i, artist_name)
        total_count = total_count + current_count
    # print("The number of times", keyword, "is said by", artist_name, "in all songs is:", total_count)
    return total_count


# Find Frequencies of keywords in one or all songs
def find_keyword_counts_in_song(data, list_of_keywords, song_index):
    """
    Takes a list of keywords and finds counts for every keyword that's in the song

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
    # print(list_of_keyword_counts)
    return list_of_keyword_counts


def find_keyword_counts_in_all_songs(data, list_of_keywords, bad_song_indices):
    """
    Takes a list of keywords and finds counts for every keyword in every song

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
    list
        a list of tuples where first value is the keyword, second value is int of occurrences
    """

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return []

    list_of_keyword_counts = []

    for i in range(len(list_of_keywords)):  # Loop through all the keywords to count
        current_cumulative_count = 0
        for j in range(len(data['songs'])):  # Loop through every song in data
            if j in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
                continue
            current_cumulative_count = current_cumulative_count + find_keyword_count_in_song(data, list_of_keywords[i], j)
        list_of_keyword_counts.append((list_of_keywords[i], current_cumulative_count))

    #print(list_of_keyword_counts)
    return list_of_keyword_counts

def find_keyword_counts_in_song_by_artist(data, list_of_keywords, song_index_, artist_name):
    """TODO"""

def find_keyword_counts_in_all_songs_by_artist(data, list_of_keywords, bad_song_indices, artist_name):
    """TODO"""

def find_pos_counts_in_song(data, song_index, pos):
    """"
    Find counts for every specified part of speech (pos) in the song. Pos' are determined by spacy's best prediction.

    Parameters
    -------
    data : json
        the json where the Genius data is stored in
    song_index : int
        the song index of the song we want to find noun counts for

    pos:  string
        the part of speech to count
    Returns
    -------
    counts : Counter
        Counter object of all nouns in the song and their counts
    """
    if pos not in {'ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SCONJ', 'SYM', 'VERB', 'X', 'SPACE'}:
        print("\"", pos, "\" is not a valid pos tag. Please enter a valid pos tag")
        return Counter()
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = remove_punctuation(lyrics)
    lyrics.lower()
    annotated_lyrics = get_spacy_nlp_object(lyrics)
    list_of_pos = []
    for token in annotated_lyrics:
        if token.pos_ == pos:
            list_of_pos.append(token.text)

    counts = Counter(list_of_pos)

    return counts

def find_noun_counts_in_all_songs(data, bad_song_indices):
    """
    Find counts for every noun in all songs

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

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return Counter()

    cumulative_counts = Counter()
    from nltk.corpus import wordnet as wn  # this takes some time, so only load it if we use this function
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    counts = Counter()
    cumulative_counts = find_all_word_counts_in_all_songs(data, counts, bad_song_indices)

    for word in list(cumulative_counts):
        if word not in nouns:
            del cumulative_counts[word]
    #print(cumulative_counts)
    return cumulative_counts

def find_noun_counts_in_song_by_artist(data, song_index, artist_name):
    """TODO"""

def find_noun_counts_in_all_songs_by_artist(data, bad_song_indices, artist_name):
    """TODO"""

def find_keyword_counts_and_compact_variants_in_song(data, counts, list_of_list_of_words, song_index):
    """TODO"""

def find_keyword_counts_and_compact_variants_in_all_songs(data, counts, list_of_list_of_words, bad_song_indices):
    """
    Returns a dictionary with the totals for each root word in list_of_list_of_words
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

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return {}


    dict_of_totals = {}
    for i in range(len(list_of_list_of_words)):
        all_count = find_all_word_counts_in_all_songs(data, counts, bad_song_indices)
        #print("All the words are: ", all_count)
        custom_count = custom_white_list_count_object(all_count, list_of_list_of_words[i])
        #print("The words after white-listing are: ", custom_count)
        total = 0
        for key in custom_count.keys():  # Loop to add up all the variants together to find total of root word
            # print("Key here is: ",custom_count.get(key))
            total = total + custom_count.get(key)
        print("\"" + list_of_list_of_words[i][0] + "\" and all its variants add up to: ", total, "\n")
        dict_of_totals[list_of_list_of_words[i][0]] = total

    #print("The final words and their variants add up to: ", dict_of_totals)
    return dict_of_totals

def find_keyword_counts_and_compact_variants_in_song_by_artist(data, counts, list_of_list_of_words, song_index, artist_name):
    """TODO"""

def find_keyword_counts_and_compact_variants_in_all_songs_by_artist(data, counts, list_of_list_of_words, bad_song_indices, artist_name):
    """
    Returns a dictionary with the totals for each root word in list_of_list_of_words
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
    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return {}

    dict_of_totals = {}
    for i in range(len(list_of_list_of_words)):
        all_count = find_all_word_counts_in_all_songs_by_artist(data, counts, bad_song_indices, artist_name)
        #print("All the words are: ", all_count)
        custom_count = custom_white_list_count_object(all_count, list_of_list_of_words[i])
        #print("The words after white-listing are: ", custom_count)
        total = 0
        for key in custom_count.keys():  # Loop to add up all the variants together to find total of root word
            # print("Key here is: ",custom_count.get(key))
            total = total + custom_count.get(key)
        #print("\"" + list_of_list_of_words[i][0] + "\" and all its variants add up to: ", total, "\n")
        dict_of_totals[list_of_list_of_words[i][0]] = total

    #print("The final words and their variants add up to: ", dict_of_totals)
    return dict_of_totals

# Find Frequency(s) of a phrase in one or more songs
def find_phrase_count_in_song(data, phrase, song_index):
    """Find phrase frequency in a song - will include ad libs (lyrics in parenthesis)"""
    phrase_count = 0
    phrase = phrase.lower()
    string_of_words = data['songs'][song_index]['lyrics']
    song_title = data['songs'][song_index]['title']
    if string_of_words is not None:
        string_of_words = string_of_words.lower()
        string_of_words = remove_headers_from_lyrics(string_of_words)
        string_of_words = remove_punctuation(string_of_words)
        string_of_words = string_of_words.replace('\u2005', ' ') # This catches weird bug I randomly found where spaces werent actually spaces...
        #print("lyrics should be good to go here:", string_of_words)
        #print(repr(string_of_words))
        #print(songIndex, "Currently looking at: ", data['songs'][songIndex]['title'])
        list_of_matches = re.findall(r'\b' + phrase + r'\b', string_of_words)
        # print(list_of_matches)
        phrase_count = len(list_of_matches)
    #print("The number of times \"" + phrase + "\" is said in \"" + song_title + "\" is: ", phrase_count)
    return phrase_count


def find_phrase_count_in_all_songs(data, phrase, bad_song_indices):
    """Find phrase in all songs"""

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return 0

    #print("Finding \"" + phrase + "\" in All Songs...")
    phrase_count = 0
    phrase = phrase.lower()
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        list_of_words = data['songs'][i]['lyrics']
        if list_of_words is not None:
            list_of_words = list_of_words.lower()
            list_of_words = remove_punctuation(list_of_words)
            # print(i, "Currently looking at: ", data['songs'][i]['title'])
            phrase_count = phrase_count + find_phrase_count_in_song(data, phrase, i)
    #print("The total number of times", phrase, "is said is: ", phrase_count, "\n")
    return phrase_count


def find_phrase_counts_in_song(data, list_of_phrases, song_index):
    """Takes a list of phrases and finds counts for every phase in the list"""
    list_of_phrase_counts = []
    for i in range(len(list_of_phrases)):
        current_phrase = list_of_phrases[i]

        list_of_phrase_counts.append((current_phrase, find_phrase_count_in_song(data, list_of_phrases[i], song_index)))
        #print(list_of_phrase_counts)

    #print(list_of_phrase_counts)
    return list_of_phrase_counts

def find_phrase_count_in_song_by_artist(data, phrase, song_index, artist_name):
    """Find phrase frequency in a song by only the artist- will include ad libs (lyrics in parenthesis)"""
    phrase_count = 0
    phrase = phrase.lower()
    string_of_words = get_only_artist_lyrics_in_song(data, song_index, artist_name)
    #print(string_of_words)
    song_title = data['songs'][song_index]['title']
    if string_of_words is not None:
        string_of_words = string_of_words.lower()
        string_of_words = remove_punctuation(string_of_words)
        print(song_index, "Currently looking at: ", data['songs'][song_index]['title'])
        list_of_matches = re.findall(r'\b' + phrase + r'\b', string_of_words)
        # print(list_of_matches)
        phrase_count = len(list_of_matches)
    # print("The number of times \"" + phrase + "\" is said in \"" + song_title + "\" by", artist_name, " is: ",
    #       phrase_count)
    return phrase_count


# Find the Song Where a Keyword or Phrase is said the most
def find_song_where_keyword_is_said_the_most(data, keyword, bad_song_indices):
    """
    TODO
    Parameters
    ----------
    data
    keyword
    bad_song_indices

    Returns
    -------

    """

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return ''

    highest_count = find_keyword_count_in_song(data, keyword, 0)
    title_of_highest_count = ''
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        current_count = find_keyword_count_in_song(data, keyword, i)
        if current_count > highest_count:
            highest_count = current_count
            title_of_highest_count = data['songs'][i]['title']
        elif current_count == highest_count:
            # TODO
            pass

    list_of_info = [highest_count, title_of_highest_count]
    # print("The song with the most occurrences of", keyword, "is: ", title_of_highest_count, "with a count of:",
    #       highest_count, "occurrences.")

    return list_of_info


def find_song_where_phrase_is_said_the_most(data, phrase, bad_song_indices):

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return ''

    highest_count = find_keyword_count_in_song(data, phrase, 0)
    title_of_highest_count = ''
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        current_count = find_phrase_count_in_song(data, phrase, i)
        if current_count > highest_count:
            highest_count = current_count
            title_of_highest_count = data['songs'][i]['title']

    list_of_info = [highest_count, title_of_highest_count]
    # print("The song with the most occurrences of", phrase, "is: ", title_of_highest_count, "with a count of:", highest_count,
    #       "occurrences.")
    return list_of_info


# Find All or Most Word Counts in specific song or every song
def find_all_word_counts_in_song(data, song_index, convert_to_list = False, counts = Counter()):
    """
    Counts how often every word occurs in a song

    Parameters
    -------
    data : json
        the json where the Genius data is stored in
    song_index : int
        index of song in the json to look at
    convert_to_list : Boolean
        If true, will return the output in a list data type, otherwise will return as Counter object
    counts : Counter
        Counter Object that will hold every word and how often it occurs, optional param

    Returns
    -------
    counts : Counter or List
        Counter Object or list (depending on convert_to_list) that will hold every word and how often it occurs
    """
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        counts = counts + Counter(lyrics)
        # print(counts)

    if convert_to_list:
        return list(counts)
    return counts


def find_all_word_counts_in_all_songs(data, cumulative_counts, bad_song_indices):
    """Counts how often every word occurs cumulatively in every song in data"""

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return Counter()

    if not is_valid_indices_list(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('['+str(i)+']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['songs']) - 1:
                print('['+str(i)+']', bad_song_indices[i])
        return Counter()

    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        cumulative_counts = find_all_word_counts_in_song(data, i, cumulative_counts)
    #    print(i,"cumulativeCounts here is: ",cumulativeCounts)

    # print("The total counts are: ", cumulativeCounts)

    return cumulative_counts


def find_most_word_counts_in_song(data, song_index, counts, words_to_omit):
    """Counts how often every word occurs in a song minus the omitted words"""
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        counts = counts + Counter(lyrics)

    for word in words_to_omit:
        if word in counts:
            del counts[word]
    return counts


def find_most_word_counts_in_all_songs(data, cumulative_counts, bad_song_indices, words_to_omit):
    """Counts how often every word occurs minus the omitted words cumulatively in every song in data"""
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        cumulative_counts = find_all_word_counts_in_song(data, i, cumulative_counts)

    for word in words_to_omit:
        if word in cumulative_counts:
            del cumulative_counts[word]
    return cumulative_counts


def find_all_word_counts_in_song_by_artist(data, song_index, counts, artist_name):
    """"Counts the frequency of every word in the song only by the specified artist"""
    listOfEachLyric = get_only_artist_lyrics_in_song(data, song_index, artist_name)
    if listOfEachLyric is not None:
        listOfEachLyric = listOfEachLyric.lower()
        listOfEachLyric = remove_punctuation(listOfEachLyric)
        listOfEachLyric = listOfEachLyric.split()
        counts = counts + Counter(listOfEachLyric)
    return counts


def find_all_word_counts_in_all_songs_by_artist(data, cumulative_counts, bad_song_indices, artist_name):
    """Counts how often every word occurs cumulatively in every song in data by only the artist specified"""
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):
            continue
        cumulative_counts = find_all_word_counts_in_song_by_artist(data, i, cumulative_counts, artist_name)
    return cumulative_counts


# Find list of songs containing the keyword or phrase
def get_list_of_songs_with_keyword(data, keyword, bad_song_indices):
    """Get list of songs that have at least 1 occurrence of the keyword"""
    listOfSongs = []
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):
            continue
        if find_keyword_count_in_song(data, keyword, i) > 0:
            listOfSongs.append(data['songs'][i]['title'])
    #print("The list of", len(listOfSongs), "song(s) containing the word \"" + keyword + "\" are: ", listOfSongs)
    return listOfSongs


def get_list_of_songs_with_phrase(data, phrase, bad_song_indices):
    """Get list of songs that have at least 1 occurrence of the phrase"""
    list_of_songs = []
    phrase = phrase.lower()
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        lyrics = data['songs'][i]['lyrics']
        lyrics = remove_headers_from_lyrics(lyrics)
        song_title = data['songs'][i]['title']
        if lyrics is not None:
            lyrics = lyrics.lower()
            lyrics = remove_punctuation(lyrics)
            lyrics = lyrics.replace('\u2005', ' ') #This catches weird bug I randomly found where spaces werent actually spaces...
            # print(i, "Currently looking at: ", data['songs'][i]['title'])
            listOfMatches = re.findall(r'\b' + phrase + r'\b', lyrics)
            # print(listOfMatches)
            phraseCount = len(listOfMatches)
            # print("The number of times \"" + phrase + "\" is said in \"" + song_title + "\" is: ", phraseCount)
            if phraseCount > 0:
                list_of_songs.append(song_title.replace('\u200b',
                                                     ''))  # the replace catches weird bug where \u200b was showing up in print(list_of_songs) entries

    #print("The list of", len(list_of_songs), "songs containing the phrase \"" + phrase + "\" are: ", list_of_songs)
    return list_of_songs

def get_list_of_songs_without_phrase(data, phrase, bad_song_indices):
    listOfAllSongs = []
    listOfSongsWithPhrase = get_list_of_songs_with_phrase(data, phrase, bad_song_indices)
    listofSongsWithoutPhrase = []
    for i in range(len(data['songs'])):
        if i in set(bad_song_indices):
            continue
        currentSongTitle = data['songs'][i]['title']
        currentSongTitle = currentSongTitle.replace('\u200b', '')
        listOfAllSongs.append(currentSongTitle)
    for i in range(len(listOfAllSongs)):
        if listOfAllSongs[i] in listOfSongsWithPhrase:
            continue
        else:
            listofSongsWithoutPhrase.append(listOfAllSongs[i])

    #print("The list of",len(listofSongsWithoutPhrase), "songs without the phrase \""+phrase+"\" are:", listofSongsWithoutPhrase)
    return listofSongsWithoutPhrase

def get_list_of_songs_with_keyword_by_artist(data, keyword, bad_song_indices, artist_name):
    """
    Gets list of songs that have at least 1 occurrence of the keyword by the artist
    """
    listOfSongs = []
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        lyrics = get_only_artist_lyrics_in_song(data, i, artist_name)
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        if keyword in lyrics:
            listOfSongs.append(data['songs'][i]['title'].replace('\u200b', ''))
    # print("The list of", len(listOfSongs), "song(s) containing the word \"" + keyword + "\" said by", artistName,
    #       "are: ", listOfSongs)

    return listOfSongs


def get_list_of_songs_with_phrase_by_artist(data, phrase, bad_song_indices, artist_name):
    """
    Gets list of songs that have at least 1 occurrence of the phrase by the artist
    """
    listOfSongs = []
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in set(bad_song_indices):  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        lyrics = get_only_artist_lyrics_in_song(data, i, artist_name)
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        listOfMatches = re.findall(r'\b' + phrase + r'\b', lyrics)
        phrase_count = len(listOfMatches)
        if phrase_count > 0:
            listOfSongs.append(data['songs'][i]['title'].replace('\u200b', ''))
    # print("The list of", len(listOfSongs), "song(s) containing the phrase \"" + phrase + "\" said by", artistName,
    #       "are: ", listOfSongs)

    return listOfSongs


# Filter Count Objects
def filter_count_object(counts, part_of_speech):
    """
    Removes words that don't fall under the part_of_speech from a Counter Object
    """

    if (part_of_speech == 'noun'):
        from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
        good_words = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    elif (part_of_speech == 'verb'):
        from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
        good_words = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
    elif (part_of_speech == 'adjective'):
        from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
        good_words = {x.name().split('.', 1)[0] for x in wn.all_synsets('a')}
    else:
        print("Invalid part of speech input")
        return counts

    for word in list(counts):  # filter out the words that aren't in good_words
        if word not in good_words:
            del counts[word]

    return counts


def custom_black_list_count_object(counts, black_list):
    """Removes words that are in the blackList from Counter Object"""
    for word in list(counts):  # filter out the words that aren't in goodWords
        if word in black_list:
            del counts[word]
    return counts


def custom_white_list_count_object(counts, white_list):
    """Removes words that are not in the whiteList from Counter Object"""
    for word in list(counts):  # filter out the words that aren't in goodWords
        if word not in white_list:
            del counts[word]
    return counts

def find_common_two_word_phrases_in_two_songs(data, song_index1, song_index2):
    """Get list of two word common phrases among both songs"""
    string1 = data['songs'][song_index1]['lyrics'].lower()
    string1 = remove_headers_from_lyrics(string1)
    string1 = remove_punctuation(string1)
    string1 = string1.replace('\n', ' ')
    string2 = data['songs'][song_index2]['lyrics'].lower()
    string2 = remove_headers_from_lyrics(string2)
    string2 = remove_punctuation(string2)
    string2 = string2.replace('\n', ' ')
    list1 = string1.split()
    list2 = string2.split()
    common_phrases = set()

    for i in range(len(list1)-1): #Loop through each 2 word phrase in song 1
        first_phrase = list1[i] + ' ' + list1[i+1]
        for j in range(len(list2)-1): #loop through each 2 word phrase in song 2
            secondPhrase = list2[j] + ' ' + list2[j+1]
            # print("First phrase: ", first_phrase)
            # print("Second phrase: ", secondPhrase)
            if first_phrase == secondPhrase:
                common_phrases.add(first_phrase)


    #print("The common 2 word phrases from both songs are: ",common_phrases)
    return common_phrases

def find_how_many_songs_each_phrase_occurs(data, bad_song_indices):
    """
    TODO
    Return dictionary with key as two word phrase and value is how many songs that phrase occurs in
    """
    # TODO
    print("5")

def get_two_word_phrases_in_song(data, song_index):
    """
    Return list of all two word phrases from the song. No duplicates
    """
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = lyrics.lower()
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.split()
    list_of_phrases = []
    for i in range(len(lyrics)-1):
        phrase = lyrics[i] + " " + lyrics[i+1]
        list_of_phrases.append(phrase)

    list_of_phrases = set(list_of_phrases)
    list_of_phrases = list(list_of_phrases)
    list_of_phrases = sorted(list_of_phrases)
    return list_of_phrases

def get_two_word_phrases_in_song_with_duplicates(data, song_index):
    """
    Return list of all two word phrases from the song
    """
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = lyrics.lower()
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.split()
    list_of_phrases = []
    for i in range(len(lyrics)-1):
        phrase = lyrics[i] + " " + lyrics[i+1]
        list_of_phrases.append(phrase)

    return list_of_phrases

def find_all_two_word_phrase_counts_in_song(data, song_index, counts):
    """

    Parameters
    ----------
    data
    song_index

    Returns
    -------

    """
    list_of_phrases = get_two_word_phrases_in_song_with_duplicates(data, song_index)

    counts = counts + Counter(list_of_phrases)
    return counts


def get_list_of_most_common_two_word_phrases_in_all_songs(data, bad_song_indices):
    """
    Returns list of every song's unique two word phrases. Duplicates mean the phrase is in more than 1 song
    """
    cumulative_list_of_phrases = []
    song_count = 0
    for i in range(len(data['songs'])):
        if i not in set(bad_song_indices):
            initial_song = i
            break
    cumulative_list_of_phrases = get_two_word_phrases_in_song(data, initial_song)  # Initial Cumulative list is just set to first song

    for i in range(initial_song+1,len(data['songs'])):  # Loop through all the songs
        if i not in set(bad_song_indices):
            song_count = song_count + 1
            #print("i here is:", i)
            currentSong = get_two_word_phrases_in_song(data, i)
            cumulative_list_of_phrases.extend(currentSong)
    z = Counter(cumulative_list_of_phrases)
    #print("Checked ", song_count, "songs")
    return z

    return cumulative_list_of_phrases

def find_most_repeated_phrases_of_any_length_in_song(data, song_index):
    """
    Will scan through a song's lyrics and try to find the most repeated phrases.
    Parameters
    ----------
    data
    song_index

    Returns
    -------

    """
    lyrics = data['songs'][song_index]['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    lyrics = lyrics.lower()
    lyrics = remove_punctuation(lyrics)
    lyrics = lyrics.split()

    list_of_all_phrases = []
    last_word_index = 0
    x = len(lyrics)

    for phrase_length in range(1, len(lyrics) + 1):
        first_word_index = 0
        last_word_index = phrase_length - 1
        for j in range(last_word_index, len(lyrics)):
            current_phrase_list = lyrics[first_word_index:first_word_index + phrase_length]
            current_phrase = ""
            for i, word in enumerate(current_phrase_list):
                if i is len(current_phrase_list) - 1:
                    current_phrase += str(word)
                else:
                    current_phrase += str(word) + " "
            list_of_all_phrases.append(current_phrase)
            first_word_index = first_word_index + 1
            last_word_index = last_word_index + 1
    print(list_of_all_phrases)
    phrases_counts = Counter(list_of_all_phrases)

    return phrases_counts


def get_list_of_artists_in_song(data, song_index):
    """
    Returns a list of all the artists on the song
    Parameters
    ----------
    data
    song_index

    Returns
    -------
    list
        list of all songs in data
    """
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
    """
    Loops through all the songs in the json, then return a alphabeticalized list with all the different artists that
    appear in the JSON

    Parameters
    ----------
    data
    bad_song_indices

    Returns
    -------

    """
    # First add the name of the JSON artist
    list_of_artists = []
    list_of_artists.append(data['name'])
    # Now Loop through all the songs and add name to list if it wasn't added before
    # First loop to check for primary artist of all songs
    for i in range(len(data["songs"])):
        if i not in set(bad_song_indices):
            current_artist = data["songs"][i]["primary_artist"]["name"]
            if current_artist not in list_of_artists:
                list_of_artists.append(current_artist)
    # Next loop to check for other featured artists on the same song
    for i in range(len(data["songs"])):
        if i not in set(bad_song_indices):
            for j in range (len(data["songs"][i]["featured_artists"])):
                current_artist = data["songs"][i]["featured_artists"][j]["name"]
                if current_artist not in list_of_artists:
                    list_of_artists.append(current_artist)
    list_of_artists.sort()
    return list_of_artists

# Primary Song Analyzer Functions
def analyze_song(data, song_index):
    """
    This function will run multiple functions to show the user interesting facts and statistics about the specified
    song.
    - Song Name
    - Primary Artist
    - Featured Artists (if any)
    - Number of words in song
    - Number of unique words in song
    - Uniqueness percent of song
    - 5 Most Repeated Words In The Song
    - 5 Most Repeated Nouns In The Song
    - 5 Most Repeated Adjectives In The Song TODO
    - 5 Most Repeated Adverbs In The Song TODO
    - 5 Most repeated 2 word phrases in the song

    - TODO Sentiment analysis ?
    -
    Parameters
    ----------
    data
    song_index

    Returns
    -------
    list
        list containing all the information about the song
    """
    song_info = []
    song_info.append(data["songs"][song_index]["title"]) # Song Name
    song_info.append(data["songs"][song_index]["artist"]) # Primary Artist

    list_of_artists = []
    for j in range(len(data["songs"][song_index]["featured_artists"])):
        list_of_artists.append(data["songs"][song_index]["featured_artists"][j]["name"])
    song_info.append(list_of_artists) # Featured Artists
    song_info.append(find_total_words_in_song(data, song_index))
    song_info.append(find_total_unique_words_in_song(data, song_index))
    song_info.append(find_uniqueness_percent_of_song(data, song_index))
    song_info.append(find_all_word_counts_in_song(data, song_index, Counter()).most_common(5))
    song_info.append(find_pos_counts_in_song(data, song_index, 'NOUN').most_common(5))

    #repeated adjectives
    song_info.append(find_pos_counts_in_song(data, song_index, 'ADJ').most_common(5))
    #repeated adverbs
    song_info.append(find_pos_counts_in_song(data, song_index, 'ADV').most_common(5))

    #repeated phrases
    song_info.append(find_all_two_word_phrase_counts_in_song(data, song_index, Counter()).most_common(5))

    print("Song name:", song_info[0])
    print("Primary Artist:", song_info[1])
    print("Featured Artists:", song_info[2])
    print("Total Words In Song:", song_info[3])
    print("Number Of Unique Words In Song:", song_info[4])
    print("Uniqueness Percent Of Song:", str(song_info[5])+'%')
    print("5 Most Repeated Words In The Song:", song_info[6])
    print("5 Most Repeated Nouns In The Song:", song_info[7])
    print("5 Most Repeated Adjectives In The Song:", song_info[8])
    print("5 Most Repeated Adverbs In The Song:", song_info[9])
    print("5 Most Repeated 2-Word Phrases In The Song:", song_info[10])

    print("\n")
    return song_info


# GUI Functions
def load_existing_presets():
    """
    First, this function will ensure that the file presets.json exists. If it doesn't, then we create it.
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
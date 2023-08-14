from song_function_definitions import remove_headers_from_lyrics, remove_punctuation
from collections import Counter


# Print Functions
def print_all_songs_in_album_from_json(data):
    """
    Prints all songs from the JSON generated from the LyricsGenius Python client search_artist function

    Parameters
    -------
    data : json
        the json where the album data is stored in

    Returns
    -------
    list
        list of all songs in the album
    """
    list_of_songs = []
    for i in range(len(data['tracks'])):
        print(i, data['tracks'][i]['song']['title'])
        list_of_songs.append(data['tracks'][i]['song']['title'].replace('\u200b', ''))
    return list_of_songs


def is_valid_indices_list_album(data, list_of_indices):
    """
    Checks if a list of indices contains only valid index values. A list is valid only if it contains indices
    between 0 and the number of songs in data - 1. Negative numbers, indices out of range, strings, lists, etc. are all
    invalid values to be inside of list_of_indices and will make function return false.

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
    if not all(
            isinstance(x, int) for x in list_of_indices):  # if bad_song_indices has invalid value(s) e.g string, double
        return False
    # Check if indices are in valid range
    max_index = len(data['tracks']) - 1
    for index in list_of_indices:
        if index < 0 or index > max_index:
            return False
    return True


# Find Frequency of keyword in one or all songs
def find_keyword_count_in_song_in_album(data, keyword, song_index):
    """
    Will check one song in the album to see how many times the keyword occurs

    Parameters
    -------
    data : json
        json with album info
    keyword : str
        keyword to check in each song
    song_index : int
        index of song to check from json

    Returns
    -------
    int
        an int with how often the keyword appears in the song
    """
    keyword_count = 0
    keyword = keyword.lower()
    lyrics = data['tracks'][song_index]['song']['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.replace('\u200b', '')  # catch weird bug where \u200b was showing up in some keywords
        lyrics = lyrics.split()
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keyword_count = keyword_count + 1
    return keyword_count


def find_keyword_count_in_all_songs_in_album(data, keyword, bad_song_indices):
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

    if not is_valid_indices_list_album(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('[' + str(i) + ']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['tracks']) - 1:
                print('[' + str(i) + ']', bad_song_indices[i])
        return 0

    keyword = keyword.lower()
    keyword_count = 0
    for i in range(len(data['tracks'])):  # Loop through every song in data
        # if current song is an empty string, don't bother trying to analyze the song and continue to next song
        if i in set(bad_song_indices):
            continue
        keyword_count = keyword_count + find_keyword_count_in_song_in_album(data, keyword, i)
    return keyword_count


def find_all_word_counts_in_all_songs_in_album(data, cumulative_counts, bad_song_indices):
    """
    Counts how often every word occurs cumulatively in every song in data

    Parameters
    -------
    data : json
        json with song info
    cumulative_counts : Counter
        the word to count in all the songs in data
    bad_song_indices : list
        list of song indices we don't want to work with

    Returns
    -------
    Counter
        Counter Object that will hold every word and how often it occurs
    """

    if not is_valid_indices_list_album(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('[' + str(i) + ']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['tracks']) - 1:
                print('[' + str(i) + ']', bad_song_indices[i])
        return Counter()

    if not is_valid_indices_list_album(data, bad_song_indices):
        print("Invalid Values in bad_song_indices, please remove them:\n")
        for i in range(len(bad_song_indices)):
            if not isinstance(bad_song_indices[i], int):
                print('[' + str(i) + ']', bad_song_indices[i])
            elif bad_song_indices[i] < 0 or bad_song_indices[i] > len(data['tracks']) - 1:
                print('[' + str(i) + ']', bad_song_indices[i])
        return Counter()

    for i in range(len(data['tracks'])):  # loop through all the songs
        # if current song is an empty string, don't bother trying to analyze the song and continue to next song
        if i in set(bad_song_indices):
            continue
        cumulative_counts = find_all_word_counts_in_song_in_album(data, i, counts=cumulative_counts)

    print("The total counts are: ", cumulative_counts)

    return cumulative_counts


def find_all_word_counts_in_song_in_album(data, song_index, convert_to_list=False, counts=Counter()):
    """
    Counts how often every word occurs in a song in an album

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
    Counter
        Counter Object that will hold every word and how often it occurs
    """
    if counts is None:
        counts = Counter()
    lyrics = data['tracks'][song_index]['song']['lyrics']
    lyrics = remove_headers_from_lyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = remove_punctuation(lyrics)
        lyrics = lyrics.split()
        counts = counts + Counter(lyrics)
        # print(counts)

    if convert_to_list:
        print("returning list here")
        return list(counts)
    return counts

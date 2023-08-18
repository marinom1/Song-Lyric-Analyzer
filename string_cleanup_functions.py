# Functions that aid in cleaning up strings
# Not meant to be used or accessed by user

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
    # punc = '''!()-[]'{};:"\,<>./?@#$%^&*_~''' #Uncomment this to remove apostrophes as well
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
    original_lyrics = data['songs'][song_index]['lyrics']

    # If there are no other features on the song, headers will not say artist name
    if ': ' + artist_name not in original_lyrics:
        # If artist name does not match Genius song owner, return error because user inputted an invalid artist name
        if artist_name == data['songs'][song_index]['artist']:
            while '[' in original_lyrics:  # While lyrics still have headers in them
                start_of_header = original_lyrics.find('[', index_pointer, len(original_lyrics))
                end_of_header = original_lyrics.find(']', start_of_header, len(original_lyrics))
                header_to_remove = original_lyrics[start_of_header:end_of_header + 1]
                original_lyrics = original_lyrics.replace(header_to_remove, '')
                if '[' not in original_lyrics:  # if no more headers to remove
                    lyrics_only_from_artist = original_lyrics

        else:
            if song_index < 0:
                print("Invalid song_index")
                pass
            else:
                print("Invalid artist name inputted by user (The artist might not have lyrics on the song)")
                print("Song name:", data['songs'][song_index]['title'])
                print("Song alleged artist:", data['songs'][song_index]['artist'])
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

    # if bad_song_indices has invalid value(s) e.g string, double
    if not all(isinstance(x, int) for x in list_of_indices):
        return False
    # Check if indices are in valid range
    max_index = len(data['songs']) - 1
    for index in list_of_indices:
        if index < 0 or index > max_index:
            return False
    return True

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

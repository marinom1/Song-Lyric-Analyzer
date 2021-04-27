import json
import os
from collections import Counter
import re


# Utility Functions
def printAllSongsFromJSON(data):
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
    listOfSongs = []
    for i in range(len(data['songs'])):
        print(i, data['songs'][i]['title'])
        listOfSongs.append(data['songs'][i]['title'].replace('\u200b', ''))
    return listOfSongs


def printBadSongsFromJSON(data, badSongIndices):
    for i in range(len(data['songs'])):
        if i not in badSongIndices:
            continue
        print(i, data['songs'][i]['title'])


def printGoodSongsFromJSON(data, badSongIndices):
    """Prints all songs that are not on the badSongIndices list. Returns list of song names that are good songs"""
    totalGoodSongs = 0
    list_of_good_songs = []
    for i in range(len(data['songs'])):
        if i in badSongIndices:
            continue
        print(i, data['songs'][i]['title'])
        totalGoodSongs = totalGoodSongs + 1
        list_of_good_songs.append(data['songs'][i]['title'])
    print("There are", totalGoodSongs, "good songs")
    return list_of_good_songs

def removePunctuation(string):
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


def writeCounterToCSV(counter, outputFileName):
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')
    fp.write('Word|Frequency\n')
    for word, count in counter.most_common():
        fp.write('{}|{}\n'.format(word, count))

    fp.close()


def writeDictToCSV(dict, outputFileName):
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')
    fp.write('Word|Frequency\n')
    for word, count in dict.items():
        fp.write('{}|{}\n'.format(word, count))
    fp.close()
    print("Finished writing dict to", outputFileName)


# Find Frequency of keyword in one or all songs
def findKeywordCountInSong(data, keyword, songIndex):
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
    lyrics = removeHeadersFromLyrics(lyrics)
    songTitle = data['songs'][songIndex]['title']
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = removePunctuation(lyrics)
        lyrics = lyrics.replace('\u200b', '')  # catch weird bug where \u200b was showing up in some keywords
        lyrics = lyrics.split()
        # print(songIndex, "Currently looking at: ", data['songs'][songIndex]['title'])
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keywordCount = keywordCount + 1
        print("The number of times \"" + keyword + "\" is said in", songTitle, " is: ", keywordCount)
    return keywordCount


def findKeywordCountInAllSongs(data, keyword, badSongIndices):
    """Will go through the entire list of songs (in data) and count how many times the keyword appears in total"""
    keyword = keyword.lower()
    keywordCount = 0
    for i in range(len(data['songs'])):  # Loop through every song in data
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        keywordCount = keywordCount + findKeywordCountInSong(data, keyword, i)
    print("The total number of times", keyword, "is said in every song is: ", keywordCount, "\n")
    return keywordCount


def findKeywordCountInSongByArtist(data, keyword, songIndex, artistName):
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
    lyrics = getOnlyArtistLyricsInSong(data, songIndex, artistName)
    songTitle = data['songs'][songIndex]['title']
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = removePunctuation(lyrics)
        lyrics = lyrics.split()
        # print(songIndex, "Currently looking at: ", data['songs'][songIndex]['title'])
        for a in range(len(lyrics)):  # Loop through the current song
            if (keyword in lyrics[a]) & (keyword == lyrics[a]):
                keywordCount = keywordCount + 1
        print("The number of times \"" + keyword + "\" is said in", songTitle, "by", artistName, "is:", keywordCount)
    return keywordCount


def findKeywordCountInAllSongsByArtist(data, keyword, badSongIndices, artistName):
    """Will check all songs to see how many times keyword was said by artist in total"""
    totalCount = 0
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in badSongIndices:
            continue
        currentCount = findKeywordCountInSongByArtist(data, keyword, i, artistName)
        totalCount = totalCount + currentCount
    print("The number of times", keyword, "is said by", artistName, "in all songs is:", totalCount)
    return totalCount


# Find Frequencies of keywords in one or all songs
def findKeywordCountsInSong(data, listOfKeywords, songIndex):
    """Takes a list of keywords and finds counts for every keyword that's in the song"""
    listOfKeywordCounts = []
    # print(listOfKeywords)
    for i in range(len(listOfKeywords)):  # Loop through all the keywords to count
        currentKeyword = listOfKeywords[i]

        listOfKeywordCounts.append((currentKeyword, findKeywordCountInSong(data, listOfKeywords[i], songIndex)))
        # print(listOfKeywordCounts)

    print(listOfKeywordCounts)
    return listOfKeywordCounts


def findKeywordCountsInAllSongs(data, listOfKeywords, badSongIndices):
    """Takes a list of keywords and finds counts for every keyword in every song"""
    listOfKeywordCounts = []

    for i in range(len(listOfKeywords)):  # Loop through all the keywords to count
        currentCumulativeCount = 0
        for j in range(len(data['songs'])):  # Loop through every song in data
            if j in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
                continue
            currentCumulativeCount = currentCumulativeCount + findKeywordCountInSong(data, listOfKeywords[i], j)
        listOfKeywordCounts.append((listOfKeywords[i], currentCumulativeCount))

    print(listOfKeywordCounts)


def findNounCountsInSong(data, songIndex):
    """"Find counts for every noun in the song

        Parameters
        -------
        data : json
            the json where the Genius data is stored in

        songIndex : int
            the song index of the song we want to find noun counts for

        Returns
        -------
        counts : Counter
            Counter object of all nouns in the song and their counts
    """

    counts = Counter()
    from nltk.corpus import wordnet as wn  # this takes some time, so we only load it if we call this function
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    counts = findAllWordCountsInSong(data, songIndex, counts)
    for word in list(counts):  # filter out the words that arent nouns
        if word not in nouns:
            del counts[word]
    print(counts)
    return counts


def findNounCountsInAllSongs(data, badSongIndices):
    """Find counts for every noun in all songs

        Parameters
        -------
        data : json
            the json where the Genius data is stored in

        badSongIndices : list
            list of song indices for songs we don't want to count for

        Returns
        -------
        cumulativeCounts : Counter
            Counter object of all nouns in every song and their cumulative counts
    """

    cumulativeCounts = Counter()
    from nltk.corpus import wordnet as wn  # this takes some time, so only load it if we use this function
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    counts = Counter()
    cumulativeCounts = findAllWordCountsInAllSongs(data, counts, badSongIndices)

    for word in list(cumulativeCounts):
        if word not in nouns:
            del cumulativeCounts[word]
    print(cumulativeCounts)
    return cumulativeCounts



def findKeywordCountsAndCompactVariantsInAllSongs(data, counts, listOfListsOfWords, badSongIndices):
    """Returns a dictionary with the totals for each root word in listOfListsOfWords
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
    listOfListsOfWords : list
        list of lists where the first entry in a list is the root word, and everything after are the word variances
    badSongIndices : list
        list of song indices we don't want to work with

    Returns
    -------
    dictOfTotals
        dictionary of each root word and their frequencies
    """
    dictOfTotals = {}
    for i in range(len(listOfListsOfWords)):
        allCount = findAllWordCountsInAllSongs(data, counts, badSongIndices)
        print("All the words are: ", allCount)
        customCount = customWhiteListCountObject(allCount, listOfListsOfWords[i])
        print("The words after white-listing are: ", customCount)
        total = 0
        for key in customCount.keys():  # Loop to add up all the variants together to find total of root word
            # print("Key here is: ",customCount.get(key))
            total = total + customCount.get(key)
        print("\"" + listOfListsOfWords[i][0] + "\" and all its variants add up to: ", total, "\n")
        dictOfTotals[listOfListsOfWords[i][0]] = total

    print("The final words and their variants add up to: ", dictOfTotals)
    return dictOfTotals


def findKeywordCountsAndCompactVariantsInAllSongsByArtist(data, counts, listOfListsOfWords, badSongIndices, artistName):
    """Returns a dictionary with the totals for each root word in listOfListsOfWords
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
        listOfListsOfWords : list
            list of lists where the first entry in a list is the root word, and everything after are the word variances
        badSongIndices : list
            list of song indices we don't want to work with

        Returns
        -------
        dictOfTotals
            dictionary of each root word and their frequencies
        """
    dictOfTotals = {}
    for i in range(len(listOfListsOfWords)):
        allCount = findAllWordCountsInAllSongsByArtist(data, counts, badSongIndices, artistName)
        print("All the words are: ", allCount)
        customCount = customWhiteListCountObject(allCount, listOfListsOfWords[i])
        print("The words after white-listing are: ", customCount)
        total = 0
        for key in customCount.keys():  # Loop to add up all the variants together to find total of root word
            # print("Key here is: ",customCount.get(key))
            total = total + customCount.get(key)
        print("\"" + listOfListsOfWords[i][0] + "\" and all its variants add up to: ", total, "\n")
        dictOfTotals[listOfListsOfWords[i][0]] = total

    print("The final words and their variants add up to: ", dictOfTotals)
    return dictOfTotals

# Find Frequency(s) of a phrase in one or more songs
def findPhraseCountInSong(data, phrase, songIndex):
    """Find phrase frequency in a song - will include ad libs (lyrics in parenthesis)"""
    phraseCount = 0
    phrase = phrase.lower()
    stringOfWords = data['songs'][songIndex]['lyrics']
    songTitle = data['songs'][songIndex]['title']
    if stringOfWords is not None:
        stringOfWords = stringOfWords.lower()
        stringOfWords = removeHeadersFromLyrics(stringOfWords)
        stringOfWords = removePunctuation(stringOfWords)
        stringOfWords = stringOfWords.replace('\u2005', ' ') # This catches weird bug I randomly found where spaces werent actually spaces...
        #print("lyrics should be good to go here:", stringOfWords)
        print(repr(stringOfWords))
        print(songIndex, "Currently looking at: ", data['songs'][songIndex]['title'])
        listOfMatches = re.findall(r'\b' + phrase + r'\b', stringOfWords)
        # print(listOfMatches)
        phraseCount = len(listOfMatches)
    print("The number of times \"" + phrase + "\" is said in \"" + songTitle + "\" is: ", phraseCount)
    return phraseCount


def findPhraseCountInAllSongs(data, phrase, badSongIndices):
    """Find phrase in all songs"""
    print("Finding \"" + phrase + "\" in All Songs...")
    phraseCount = 0
    phrase = phrase.lower()
    for i in range(len(data['songs'])):  # loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        listOfWords = data['songs'][i]['lyrics']
        if listOfWords is not None:
            listOfWords = listOfWords.lower()
            listOfWords = removePunctuation(listOfWords)
            # print(i, "Currently looking at: ", data['songs'][i]['title'])
            phraseCount = phraseCount + findPhraseCountInSong(data, phrase, i)
    print("The total number of times", phrase, "is said is: ", phraseCount, "\n")
    return phraseCount


def findPhraseCountsInSong(data, listOfPhrases, songIndex):
    """Takes a list of phrases and finds counts for every phase in the list"""
    listOfPhraseCounts = []
    for i in range(len(listOfPhrases)):
        currentPhrase = listOfPhrases[i]

        listOfPhraseCounts.append((currentPhrase, findPhraseCountInSong(data, listOfPhrases[i], songIndex)))
        print(listOfPhraseCounts)

    print(listOfPhraseCounts)


def findPhraseCountInSongByArtist(data, phrase, songIndex, artistName):
    """Find phrase frequency in a song by only the artist- will include ad libs (lyrics in parenthesis)"""
    phraseCount = 0
    phrase = phrase.lower()
    stringOfWords = getOnlyArtistLyricsInSong(data, songIndex, artistName)
    print(stringOfWords)
    songTitle = data['songs'][songIndex]['title']
    if stringOfWords is not None:
        stringOfWords = stringOfWords.lower()
        stringOfWords = removePunctuation(stringOfWords)
        print(songIndex, "Currently looking at: ", data['songs'][songIndex]['title'])
        listOfMatches = re.findall(r'\b' + phrase + r'\b', stringOfWords)
        # print(listOfMatches)
        phraseCount = len(listOfMatches)
    print("The number of times \"" + phrase + "\" is said in \"" + songTitle + "\" by", artistName, " is: ",
          phraseCount)
    return phraseCount


# Find the Song Where a Keyword or Phrase is said the most
def findSongWhereKeywordIsSaidTheMost(data, keyword, badSongIndices):
    highestCount = findKeywordCountInSong(data, keyword, 0)
    titleOfHighestCount = data['songs'][0]['title']
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        currentCount = findKeywordCountInSong(data, keyword, i)
        if (currentCount > highestCount):
            highestCount = currentCount
            titleOfHighestCount = data['songs'][i]['title']

    listOfInfo = [highestCount, titleOfHighestCount]
    print("The song with the most occurrences of", keyword, "is: ", titleOfHighestCount, "with a count of:",
          highestCount, "occurrences.")
    return listOfInfo


def findSongWherePhraseIsSaidTheMost(data, phrase, badSongIndices):
    highestCount = findKeywordCountInSong(data, phrase, 0)
    titleOfHighestCount = data['songs'][0]['title']
    for i in range(len(data['songs'])):  # Loop through all the songs
        if i in badSongIndices:  # if current song is an empty string, don't bother trying to analyze the song and continue to next song
            continue
        currentCount = findPhraseCountInSong(data, phrase, i)
        if (currentCount > highestCount):
            highestCount = currentCount
            titleOfHighestCount = data['songs'][i]['title']

    listOfInfo = [highestCount, titleOfHighestCount]
    print("The song with the most occurrences of", phrase, "is: ", titleOfHighestCount, "with a count of:", highestCount,
          "occurrences.")
    return listOfInfo


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
    lyrics = removeHeadersFromLyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = removePunctuation(lyrics)
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
    lyrics = removeHeadersFromLyrics(lyrics)
    if lyrics is not None:
        lyrics = lyrics.lower()
        lyrics = removePunctuation(lyrics)
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
    listOfEachLyric = getOnlyArtistLyricsInSong(data, songIndex, artistName)
    if listOfEachLyric is not None:
        listOfEachLyric = listOfEachLyric.lower()
        listOfEachLyric = removePunctuation(listOfEachLyric)
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
        if findKeywordCountInSong(data, keyword, i) > 0:
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
        lyrics = removeHeadersFromLyrics(lyrics)
        songTitle = data['songs'][i]['title']
        if lyrics is not None:
            lyrics = lyrics.lower()
            lyrics = removePunctuation(lyrics)
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
        lyrics = getOnlyArtistLyricsInSong(data, i, artistName)
        lyrics = lyrics.lower()
        lyrics = removePunctuation(lyrics)
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
        lyrics = getOnlyArtistLyricsInSong(data, i, artistName)
        lyrics = lyrics.lower()
        lyrics = removePunctuation(lyrics)
        listOfMatches = re.findall(r'\b' + phrase + r'\b', lyrics)
        phraseCount = len(listOfMatches)
        if phraseCount > 0:
            listOfSongs.append(data['songs'][i]['title'].replace('\u200b', ''))
    print("The list of", len(listOfSongs), "song(s) containing the phrase \"" + phrase + "\" said by", artistName,
          "are: ", listOfSongs)

    return listOfSongs


# Filter Count Objects
def filterCountObject(counts, partOfSpeech):
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


def getOnlyArtistLyricsInSong(data, songIndex, artistName):
    """Will go through a song and get only the lyrics said by the artist, returns string"""
    lyricsOnlyFromArtist = ''
    indexPointer = 0
    startOfVerse = 0
    endOfVerse = 1
    lyrics = data['songs'][songIndex]['lyrics']
    # print("lyrics here is:",lyrics,"from song:",data['songs'][songIndex]['title'])
    if ': ' + artistName not in lyrics:  # If there are no other features on the song, headers will not say artist name
        if artistName == data['songs'][songIndex]['artist']:  # If artist name does not match Genius song owner, return error because user inputted an invalid artist name
            print(artistName == data['songs'][songIndex]['artist'])
            while (True):
                startOfHeader = lyrics.find('[', indexPointer, len(lyrics))
                endOfHeader = lyrics.find(']', startOfHeader, len(lyrics))
                headerToRemove = lyrics[startOfHeader:endOfHeader + 1]
                # print("The header to remove is:",headerToRemove)
                lyrics = lyrics.replace(headerToRemove, '')
                # print(lyrics)
                if '[' not in lyrics:  # if no more headers to remove
                    # print("No more headers to remove.")
                    # print(lyrics)
                    return lyrics
        else:
            print("Invalid artist name inputted by user")

    else:  # The song has 1 or more features
        while (True):
            startOfVerse = lyrics.find((': ' + artistName), indexPointer, len(lyrics)) + len(
                artistName) + 4  # logic to skip the header and get right to lyrics
            endOfVerse = lyrics.find('\n\n', startOfVerse, len(lyrics))
            if endOfVerse == -1:  # If verse is last in the whole song, \n\n wont be found
                endOfVerse = len(lyrics)

            # print("startOfVerse:",startOfVerse,"endOfVerse:",endOfVerse)
            verse = lyrics[startOfVerse:endOfVerse]
            # print("The verse is:",verse)
            indexPointer = endOfVerse
            lyricsOnlyFromArtist = lyricsOnlyFromArtist + '\n' + verse

            if ': ' + artistName not in lyrics[indexPointer:len(lyrics)]:
                # print("No more verses from", artistName)
                break

        # print(lyricsOnlyFromArtist)
        return lyricsOnlyFromArtist


def getNumberOfWordsInSong(data, songIndex):
    """Count how many words are in a song"""
    total = 0
    lyrics = data['songs'][songIndex]['lyrics']
    lyrics = removeHeadersFromLyrics(lyrics)
    lyrics = lyrics.split()
    total = len(lyrics)
    return total


def removeHeadersFromLyrics(lyrics):
    """Gets lyrics without the header tags, returns string"""
    indexPointer = 0
    while (13 == 13):
        startOfHeader = lyrics.find('[', indexPointer, len(lyrics))
        endOfHeader = lyrics.find(']', startOfHeader, len(lyrics))
        headerToRemove = lyrics[startOfHeader:endOfHeader + 1]
        lyrics = lyrics.replace(headerToRemove, '')
        if '[' not in lyrics:  # if no more headers to remove
            return lyrics

def writeCounterToCustomCSV(counts, outputFileName):
    """Writes CSV in way that wordart.com accepts it as an import"""
    fp = open(outputFileName, encoding='utf-8-sig', mode='w')

    for word, count in counts.most_common(20):
        fp.write('{};{}\n'.format(word, count))

    fp.close()

def findCommonTwoWordPhrasesInTwoSongs(data, songIndex1, songIndex2):
    """Get list of two word common phrases among both songs"""
    string1 = data['songs'][songIndex1]['lyrics'].lower()
    string1 = removeHeadersFromLyrics(string1)
    string1 = removePunctuation(string1)
    string1 = string1.replace('\n', ' ')
    string2 = data['songs'][songIndex2]['lyrics'].lower()
    string2 = removeHeadersFromLyrics(string2)
    string2 = removePunctuation(string2)
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
    lyrics = removeHeadersFromLyrics(lyrics)
    lyrics = lyrics.lower()
    lyrics = removePunctuation(lyrics)
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
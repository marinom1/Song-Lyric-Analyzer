import unittest
from functionDefinitions import *

# Lyrics_Khalid_all.json is testing input
with open('Lyrics_Khalid_all.json') as json_file:
    data = json.load(json_file)


class TestPrintFunctions(unittest.TestCase):

    def test_print_all_songs_from_json(self):
        list_of_songs = print_all_songs_from_json(data)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[10], 'OTW')
        self.assertEqual(list_of_songs[147], 'Maranatha')
        self.assertEqual(len(list_of_songs), 148)

    def test_print_bad_songs_from_json(self):
        khalid_bad_song_indices = [75, 74, 72, 70, 69, 48, 45, 38, 33]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], 'Location (Remix)')
        self.assertEqual(list_of_songs[1], 'Right Back (Remix)')
        self.assertEqual(list_of_songs[8], 'Why Don’t You Come On')
        self.assertEqual(len(list_of_songs), 9)

    def test_print_good_songs_from_json(self):
        khalid_bad_song_indices = [75, 74, 72, 70, 69, 48, 45, 38, 33]
        self.assertTrue(print_good_songs_from_json(data, khalid_bad_song_indices))
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[33], 'Motion')
        self.assertEqual(list_of_songs[37], 'Right Back')
        self.assertEqual(len(list_of_songs), 139)


class TestHelperFunctions(unittest.TestCase):
    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation('Let\'s'), 'Lets')
        self.assertEqual(remove_punctuation('abcd123@email.com'), 'abcd123emailcom')
        self.assertEqual(remove_punctuation('I\'ve been on the low, I been taking my time'), 'Ive been on the low I been taking my time')
        self.assertEqual(remove_punctuation('I\'ve been !on" t;:he lo@?<.>w, I been tak[]ing m%$y ti-me'), 'Ive been on the low I been taking my time')

    def test_remove_headers_from_lyrics(self):
        lyrics = "[Pre-Chorus: Logic]\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine (Who can relate? Woo)\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine\n\n[Chorus: Logic]\nI don't wanna be alive, I don't wanna be alive"
        self.assertEqual(remove_headers_from_lyrics(lyrics), "\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine (Who can relate? Woo)\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine\n\n\nI don't wanna be alive, I don't wanna be alive")
        self.assertEqual(remove_headers_from_lyrics('[Chorus]Lyrics1\n[Verse 1]Lyrics2\n[Outro]Goodbye World!'), 'Lyrics1\nLyrics2\nGoodbye World!')

    def test_get_only_artist_lyrics_in_song(self):
        self.assertEqual(get_only_artist_lyrics_in_song(data, 0, 'Khalid'), '\nPain don\'t hurt the same, I know\nThe lane I travel feels alone\nBut I\'m moving \'til my legs give out\nAnd I see my tears melt in the snow\nBut I don\'t wanna cry, I don\'t wanna cry anymore\nI wanna feel alive, I don\'t even wanna die anymore\nOh, I don\'t wanna\nI don\'t wanna\nI don\'t even wanna die anymore')
        self.assertEqual(get_only_artist_lyrics_in_song(data, 0, 'Eminem'), '')
        self.assertEqual(get_only_artist_lyrics_in_song(data, -1, 'Khalid'), '')

class TestCSVFunctions(unittest.TestCase):
    # TODO
    def test_write_counter_to_csv(self):
        self.assertEqual(True, True)

    def test_write_dict_to_csv(self):
        self.assertEqual(True, True)

class TestKeywordFunctions(unittest.TestCase):

    def test_find_keyword_count_in_song(self):
        self.assertEqual(find_keyword_count_in_song(data, 'alive', 0), 13)
        self.assertEqual(find_keyword_count_in_song(data, 'Alive', 0), 13)
        self.assertEqual(find_keyword_count_in_song(data, 'Chorus', 0), 0)
        self.assertEqual(find_keyword_count_in_song(data, 'What\'s', 0), 0)
        self.assertEqual(find_keyword_count_in_song(data, 'Whats', 0), 2)

    def test_find_keyword_count_in_all_songs(self):
        self.assertEqual(find_keyword_count_in_all_songs(data, 'love', []), 611)
        self.assertEqual(find_keyword_count_in_all_songs(data, 'love', [1]), 606)

    def test_find_keyword_count_in_song_by_artist(self):
        self.assertEqual(find_keyword_count_in_song_by_artist(data, 'alive', 0, 'Logic'), 12)
        self.assertEqual(find_keyword_count_in_song_by_artist(data, 'alive', 0, 'Khalid'), 1)
        self.assertEqual(find_keyword_count_in_song_by_artist(data, 'alive', 0, 'Alessia Cara'), 0)
        self.assertRaises(TypeError, find_keyword_count_in_song_by_artist(data, 'alive', -1, 'Khalid'))
        self.assertEqual(find_keyword_count_in_song_by_artist(data, 'salmon', 0, 'Khalid'), 0)
        self.assertEqual(find_keyword_count_in_song_by_artist(data, 'alive', 0, 'Eminem'), 0)

    def test_find_keyword_count_in_all_songs_by_artist(self):
        self.assertEqual(find_keyword_count_in_all_songs_by_artist(data, 'alive', [], 'Khalid'), 50)
        self.assertEqual(find_keyword_count_in_all_songs_by_artist(data, 'alive', [], 'Eminem'), 0)
        self.assertEqual(find_keyword_count_in_all_songs_by_artist(data, 'alive', [0], 'Khalid'), 49)

if __name__ == '__main__':
    unittest.main()

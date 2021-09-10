import unittest
unittest.TestLoader.sortTestMethodsUsing = None
from functionDefinitions import *

# Lyrics_Khalid_all.json is testing input
with open('Lyrics_Khalid_all.json') as json_file:
    data = json.load(json_file)


class TestPrintFunctions(unittest.TestCase):

    def setUp(self): # Can make files here, and delete them in tearDown
        pass

    def tearDown(self):
        pass

    def test_print_all_songs_from_json_valid_input(self):
        list_of_songs = print_all_songs_from_json(data)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[10], 'OTW')
        self.assertEqual(list_of_songs[147], 'Maranatha')
        self.assertEqual(len(list_of_songs), 148)


    def test_print_bad_songs_from_json_ordered_indices(self):
        khalid_bad_song_indices = [33, 38, 45, 48, 69, 70, 72, 74, 75]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], 'Location (Remix)')
        self.assertEqual(list_of_songs[1], 'Right Back (Remix)')
        self.assertEqual(list_of_songs[8], 'Why Don’t You Come On')
        self.assertEqual(len(list_of_songs), 9)

    def test_print_bad_songs_from_json_reverse_ordered_indices(self):
        khalid_bad_song_indices = [75, 74, 72, 70, 69, 48, 45, 38, 33]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], 'Why Don’t You Come On')
        self.assertEqual(list_of_songs[1], 'Perfect')
        self.assertEqual(list_of_songs[8], 'Location (Remix)')
        self.assertEqual(len(list_of_songs), 9)

    def test_print_bad_songs_from_json_unordered_indices(self):
        khalid_bad_song_indices = [38, 33, 72, 48, 70, 69, 45, 75, 74]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], 'Right Back (Remix)')
        self.assertEqual(list_of_songs[1], 'Location (Remix)')
        self.assertEqual(list_of_songs[8], 'Perfect')
        self.assertEqual(len(list_of_songs), 9)

    def test_print_bad_songs_from_json_empty_indices_list(self):
        khalid_bad_song_indices = []
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_bad_songs_from_json_string_values_in_list(self):
        khalid_bad_song_indices = ['1-800-273-8255', 'Young Dumb & Broke', 'Right Back', 59, 73]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_bad_songs_from_json_some_out_of_range_int_values_in_list(self):
        khalid_bad_song_indices = [-1, 0, 50, 100, 300]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_bad_songs_from_json_all_out_of_index_int_values_in_list(self):
        khalid_bad_song_indices = [-1, 300, 555]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_bad_songs_from_json_repeated_valid_values(self):
        khalid_bad_song_indices = [24, 24, 25, 29, 29, 89]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, ["Reasons", "Cold Blooded", "Winter", "wildflower (rough)"])

    def test_print_bad_songs_from_json_invalid_values_with_repeated_valid_values(self):
        khalid_bad_song_indices = [0, 'Seven', 0, 1, 2, 2, 9, 11, 21.5, 18]
        list_of_songs = print_bad_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_good_songs_from_json_ordered_indices(self):
        khalid_bad_song_indices = [33, 38, 45, 48, 69, 70, 72, 74, 75]
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[8], 'Coaster')
        self.assertEqual(list_of_songs[33], 'Motion')
        self.assertEqual(len(list_of_songs), 139)

    def test_print_good_songs_from_json_reverse_ordered_indices(self):
        khalid_bad_song_indices = [75, 74, 72, 70, 69, 48, 45, 38, 33]
        self.assertTrue(print_good_songs_from_json(data, khalid_bad_song_indices))
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[33], 'Motion')
        self.assertEqual(list_of_songs[37], 'Right Back')
        self.assertEqual(len(list_of_songs), 139)

    def test_print_good_songs_from_json_empty_indices_list(self):
        khalid_bad_song_indices = []
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[33], 'Location (Remix)')
        self.assertEqual(list_of_songs[37], 'Bad Luck')
        self.assertEqual(len(list_of_songs), 148)

    def test_print_good_songs_from_json_string_values_in_list(self):
        khalid_bad_song_indices = ['1-800-273-8255', 'Young Dumb & Broke', 'Right Back', 59, 73]
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_good_songs_from_json_some_out_of_range_int_values_in_list(self):
        khalid_bad_song_indices = [-1, 0, 50, 100, 300]
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_good_songs_from_json_all_out_of_range_int_values_in_list(self):
        khalid_bad_song_indices = [-1, 300, 555]
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

    def test_print_good_songs_from_json_repeated_valid_values(self):
        khalid_bad_song_indices = [24, 24, 25, 29, 29, 89]
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs[0], '1-800-273-8255' )
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[24], 'My Bad')
        self.assertEqual(len(list_of_songs), 144)

    def test_print_good_songs_from_json_invalid_values_with_repeated_valid_values(self):
        khalid_bad_song_indices = [0, 'Seven', 0, 1, 2, 2, 9, 11, 21.5, 18]
        list_of_songs = print_good_songs_from_json(data, khalid_bad_song_indices)
        self.assertEqual(list_of_songs, [])

class TestHelperFunctions(unittest.TestCase):
    def test_remove_duplicate_valid_indices(self):
        self.assertEqual(remove_duplicate_valid_indices([1,1,2,2,3,3,4,4]), [1,2,3,4])
        self.assertEqual(remove_duplicate_valid_indices([1, 1, 1,1,1,1,1,1]), [1])
        self.assertEqual(remove_duplicate_valid_indices([]), [])
        self.assertEqual(remove_duplicate_valid_indices([1,2,3,4]), [1,2,3,4])
        self.assertRaises(TypeError, remove_duplicate_valid_indices(["Leg", "Arm"]))

    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation('Toast'), 'Toast')
        self.assertEqual(remove_punctuation('Let\'s'), 'Lets')
        self.assertEqual(remove_punctuation('abcd123@email.com'), 'abcd123emailcom')
        self.assertEqual(remove_punctuation('I\'ve been on the low, I been taking my time'), 'Ive been on the low I been taking my time')
        self.assertEqual(remove_punctuation('I\'ve been !on" t;:he lo@?<.>w, I been tak[]ing m%$y ti-me'), 'Ive been on the low I been taking my time')

    def test_remove_headers_from_lyrics(self):
        lyrics = "[Pre-Chorus: Logic]\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine (Who can relate? Woo)\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine\n\n[Chorus: Logic]\nI don't wanna be alive, I don't wanna be alive"
        self.assertEqual(remove_headers_from_lyrics(lyrics), "\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine (Who can relate? Woo)\nI've been on the low, I been taking my time\nI feel like I'm out of my mind\nIt feel like my life ain't mine\n\n\nI don't wanna be alive, I don't wanna be alive")
        self.assertEqual(remove_headers_from_lyrics('[Chorus]Lyrics1\n[Verse 1]Lyrics2\n[Outro]Goodbye World!'), 'Lyrics1\nLyrics2\nGoodbye World!')
        lyrics = ""
        self.assertEqual(remove_headers_from_lyrics(lyrics), "")

    def test_get_only_artist_lyrics_in_song(self):
        self.assertEqual(get_only_artist_lyrics_in_song(data, 0, 'Khalid'), '\nPain don\'t hurt the same, I know\nThe lane I travel feels alone\nBut I\'m moving \'til my legs give out\nAnd I see my tears melt in the snow\nBut I don\'t wanna cry, I don\'t wanna cry anymore\nI wanna feel alive, I don\'t even wanna die anymore\nOh, I don\'t wanna\nI don\'t wanna\nI don\'t even wanna die anymore')
        self.assertEqual(get_only_artist_lyrics_in_song(data, 0, 'Eminem'), '')
        self.assertEqual(get_only_artist_lyrics_in_song(data, -1, 'Khalid'), '')

    def test_is_valid_list_valid_values(self):
        self.assertEqual(is_valid_indices_list(data, [0, 1, 2, 3, 147]), True)
        self.assertEqual(is_valid_indices_list(data, [0, 12, 147, 20, 71]), True)

    def test_is_valid_list_out_of_index_int_values(self):
        self.assertEqual(is_valid_indices_list(data, [-1,148]), False)

    def test_is_valid_list_mixed_values_in_range_and_out_of_range(self):
        self.assertEqual(is_valid_indices_list(data, [-1,0, 1, 2, 3, 147, 148]), False)

    def test_is_valid_list_empty_list(self):
        self.assertEqual(is_valid_indices_list(data, []), True)

    def test_is_valid_list_string_values(self):
        self.assertEqual(is_valid_indices_list(data, ['1-800-273-8255', 'Young Dumb & Broke', 'Motion']), False)

    def test_is_valid_list_double_values(self):
        self.assertEqual(is_valid_indices_list(data, [1.0, 2.0, 3.0, 6.0]), False)

    def test_find_total_words_in_song(self):
        self.assertEqual(find_total_words_in_song(data, 0), 542)
        self.assertEqual(find_total_words_in_song(data, 1), 266)

    def test_find_total_words_in_song_by_artist(self):
        self.assertEqual(find_total_words_in_song_by_artist(data, 0, 'Khalid'), 63)
        self.assertEqual(find_total_words_in_song_by_artist(data, 1, 'Khalid'), 266)

    def test_find_total_unqiue_words_in_song(self):
        self.assertEqual(find_total_unique_words_in_song(data, 0), 151)
        self.assertEqual(find_total_unique_words_in_song(data, 1), 72)

    def test_find_total_unqiue_words_in_song_by_artist(self):
        self.assertEqual(find_total_unique_words_in_song_by_artist(data, 0, 'Khalid'), 33)
        self.assertEqual(find_total_unique_words_in_song_by_artist(data, 1, 'Khalid'), 72)

    def test_find_uniqueness_percent_of_song(self):
        self.assertEqual(find_uniqueness_percent_of_song(data, 0), 27.8598)
        self.assertEqual(find_uniqueness_percent_of_song(data, 1), 27.0677)

    def test_find_uniqueness_percent_of_song_by_artist(self):
        """TODO"""

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
        self.assertEqual(find_keyword_count_in_all_songs(data, 'love', [-1, 0, 1, "Eminem", 25]), 0)

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

    def test_find_keyword_counts_in_song(self):
        self.assertEqual(find_keyword_counts_in_song(data, ['alive', 'love', 'salmon'], 0), [('alive', 13), ('love', 0), ('salmon', 0)])
        self.assertEqual(find_keyword_counts_in_song(data, ['Alive', 'Love', 'Salmon'], 0), [('Alive', 13), ('Love', 0), ('Salmon', 0)])

    def test_find_keyword_counts_in_all_songs(self):
        self.assertEqual(find_keyword_counts_in_all_songs(data, ['alive', 'love', 'salmon'], []), [('alive', 70), ('love', 611), ('salmon', 0)])
        self.assertEqual(find_keyword_counts_in_all_songs(data, ['Alive', 'Love', 'Salmon'], []), [('Alive', 70), ('Love', 611), ('Salmon', 0)])

    def test_find_noun_counts_in_song(self):
        # TODO
        self.assertEqual(True, True)

    def test_find_noun_counts_in_all_songs(self):
        # TODO
        self.assertEqual(True, True)

    def test_find_keyword_counts_and_compact_variants_in_all_songs(self):
        # TODO
        self.assertEqual(True, True)

    def test_find_keyword_counts_and_compact_variants_in_all_songs_by_artist(self):
        # TODO
        self.assertEqual(True, True)

    def test_find_song_where_keyword_is_said_the_most(self):
        self.assertEqual(find_song_where_keyword_is_said_the_most(data, 'alive', []), [21, 'Keep Me'])
        self.assertEqual(find_song_where_keyword_is_said_the_most(data, 'salmon', []), [0, ''])

class TestPhraseFunctions(unittest.TestCase):

    def test_find_phrase_count_in_song(self):
        self.assertEqual(find_phrase_count_in_song(data, 'my time', 0), 6)
        self.assertEqual(find_phrase_count_in_song(data, 'Chorus: Logic', 0), 0)
        self.assertEqual(find_phrase_count_in_song(data, 'And let me tell you why', 0), 1)

    def test_find_phrase_count_in_all_songs(self):
        self.assertEqual(find_phrase_count_in_all_songs(data, 'my time', []), 16)
        self.assertEqual(find_phrase_count_in_all_songs(data, 'my time', [0]), 10)

    def test_find_phrase_counts_in_song(self):
        self.assertEqual(find_phrase_counts_in_song(data, ['my time','on the low', 'who can relate'] , 0), [('my time', 6), ('on the low', 6), ('who can relate', 3)])

    def test_find_song_where_phrase_is_said_the_most(self):
        self.assertEqual(find_song_where_phrase_is_said_the_most(data, 'i love you', []), [2, 'I Be On The Way'])

if __name__ == '__main__':
    unittest.main()

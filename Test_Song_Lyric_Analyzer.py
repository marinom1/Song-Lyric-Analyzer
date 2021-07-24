import unittest
import json
from functionDefinitions import *

# Lyrics_Khalid_all.json is testing input
with open('Lyrics_Khalid_all.json') as json_file: data = json.load(json_file)

class TestPrintFunctions(unittest.TestCase):

    def test_print_all_songs_from_json(self):
        list_of_songs = print_all_songs_from_json(data)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[10], 'OTW')
        self.assertEqual(list_of_songs[147], 'Maranatha')
        self.assertEqual(len(list_of_songs), 148)

    def test_print_bad_songs_from_json(self):
        khalidBadSongIndices = [75, 74, 72, 70, 69, 48, 45, 38, 33]
        list_of_songs = print_bad_songs_from_json(data, khalidBadSongIndices)
        self.assertEqual(list_of_songs[0], 'Location (Remix)')
        self.assertEqual(list_of_songs[1], 'Right Back (Remix)')
        self.assertEqual(list_of_songs[8], 'Why Don’t You Come On')
        self.assertEqual(len(list_of_songs), 9)

    def test_print_good_songs_from_json(self):
        khalidBadSongIndices = [75, 74, 72, 70, 69, 48, 45, 38, 33]
        list_of_songs = print_good_songs_from_json(data, khalidBadSongIndices)
        self.assertEqual(list_of_songs[0], '1-800-273-8255')
        self.assertEqual(list_of_songs[1], 'Young Dumb & Broke')
        self.assertEqual(list_of_songs[33], 'Motion')
        self.assertEqual(list_of_songs[37], 'Right Back')
        self.assertEqual(len(list_of_songs), 139)

class TestKeywordFunctions(unittest.TestCase):

    def test_something2(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()

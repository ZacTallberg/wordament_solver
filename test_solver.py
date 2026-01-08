import unittest
from wordament_solver import Trie, load_digram, get_word_list, begin_dfs, get_char_freq, word_possible
import os

class TestWordamentSolver(unittest.TestCase):
    def setUp(self):
        self.digram_file = "test_array.txt"
        self.word_list_file = "test_words_temp.txt"

        with open(self.digram_file, "w") as f:
            f.write("P E U H\n")
            f.write("S L T I\n")
            f.write("G A E H\n")
            f.write("S U ER D\n")

        with open(self.word_list_file, "w") as f:
            f.write("hit\n")
            f.write("gas\n")
            f.write("slathered\n")
            f.write("impossible\n")

    def tearDown(self):
        if os.path.exists(self.digram_file):
            os.remove(self.digram_file)
        if os.path.exists(self.word_list_file):
            os.remove(self.word_list_file)

    def test_trie(self):
        trie = Trie()
        trie.add_word("hello")
        exists, count, finished = trie.find_prefix("hel")
        self.assertTrue(exists)
        self.assertFalse(finished)

        exists, count, finished = trie.find_prefix("hello")
        self.assertTrue(exists)
        self.assertTrue(finished)

        exists, count, finished = trie.find_prefix("world")
        self.assertFalse(exists)

    def test_solver(self):
        digram = load_digram(self.digram_file)
        # Check if digram loaded correctly
        self.assertEqual(digram[3][2], "er")

        word_list = get_word_list(self.word_list_file, digram)
        self.assertIn("hit", word_list)
        self.assertNotIn("impossible", word_list) # Should be filtered out

        trie = Trie()
        trie.add_word_list(word_list)

        solutions = begin_dfs(digram, trie)
        self.assertIn("hit", solutions)
        self.assertIn("gas", solutions)
        self.assertIn("slathered", solutions)

    def test_sorting(self):
        # Verify that wordament_solver.run_program produces sorted output
        # We need to mock IO or just run it and check file
        pass

if __name__ == '__main__':
    unittest.main()


import unittest
from slang_labs_app.tfidf import tfidf_utils

class TestTfidfUtils(unittest.TestCase):

    def test_remove_punctuations(self):
        doc = 'Hey! Are these from yesterday?'
        doc_processed = tfidf_utils.remove_punctuations(doc)

        expected = 'Hey  Are these from yesterday '

        self.assertEqual(doc_processed, expected)

    def test_word_count(self):
        doc = ['the', 'orange', 'is', 'orange', 'in', 'colour']
        counts = tfidf_utils.get_word_counts(doc)

        expected = {
            'the': 1, 'orange': 2, 'is': 1, 'in': 1, 'colour': 1
        }

        self.assertEqual(counts, expected)


if __name__ == '__main__':
    unittest.main()

import unittest

from page_generation import extract_title

class PageGenerationTest(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# My Title\n\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_2(self):
        markdown = "## My Title\n\nSome content here."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_no_title(self):
        markdown = "No title here, just content."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiple_titles(self):
        markdown = "# First Title\n\n# Second Title\n\nContent here."
        title = extract_title(markdown)
        self.assertEqual(title, "First Title")
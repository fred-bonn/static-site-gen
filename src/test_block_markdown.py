import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestSplitBlocks(unittest.TestCase):
    def test_single_block_no_delimiters(self):
        markdown = "This is a single block"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is a single block"])

    def test_two_blocks_with_double_newline(self):
        markdown = "First block\n\nSecond block"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First block", "Second block"])

    def test_multiple_blocks(self):
        markdown = "Block 1\n\nBlock 2\n\nBlock 3"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block 1", "Block 2", "Block 3"])

    def test_leading_whitespace_removed(self):
        markdown = "  \n\n  First block\n\nSecond block  "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First block", "Second block"])

    def test_trailing_whitespace_removed(self):
        markdown = "First block  \n\n  Second block"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First block", "Second block"])

    def test_empty_blocks_ignored(self):
        markdown = "First\n\n\n\nSecond"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First", "Second"])

    def test_only_whitespace_blocks_ignored(self):
        markdown = "First\n\n   \n\nSecond"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First", "Second"])

    def test_empty_string(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_only_newlines(self):
        markdown = "\n\n\n"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_blocks_with_internal_newlines_preserved(self):
        markdown = "Line 1\nLine 2\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Line 1\nLine 2", "Block 2"])

    def test_multiple_consecutive_delimiters(self):
        markdown = "Block 1\n\n\n\nBlock 2"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block 1", "Block 2"])

    def test_blocks_with_tabs_and_spaces(self):
        markdown = "\tBlock 1\t\n\n  Block 2  "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block 1", "Block 2"])

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        result = markdown_to_blocks(markdown)
        self.assertEqual(
            result,
            [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_header_block(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###Heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("``\ncode\n``"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```code\n```"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("<Quote"), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n-Item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1> Item 1\n2> Item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 2\n2. Item 3"), BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()


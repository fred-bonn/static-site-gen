import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestNodeSplitter(unittest.TestCase):
    def test_split_nodes(self):
        nodes = [TextNode("This is a *bold* node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ])

    def test_split_nodes_multiple(self):
        nodes = [TextNode("This is a *bold* and *another bold* node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ])

    def test_split_nodes_mixed_delimiters(self):
        nodes = [TextNode("This is a *bold* and _italic_ node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and _italic_ node", TextType.TEXT)
        ])
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" node", TextType.TEXT)
        ])

    def test_split_nodes_no_delimiter(self):
        nodes = [TextNode("This is a bold node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a bold node", TextType.TEXT)
        ])

    def test_split_nodes_unmatched_delimiter(self):
        nodes = [TextNode("This is a *bold node", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertTrue("missing closing deliminiter" in str(context.exception))

    def test_split_nodes_non_text_node(self):
        nodes = [TextNode("This is a bold node", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a bold node", TextType.BOLD)
        ])

    def test_split_nodes_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_split_nodes_delimiter_at_edge(self):
        nodes = [TextNode("This is *bold at edge*", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold at edge", TextType.BOLD)
        ])

if __name__ == "__main__":
    unittest.main()
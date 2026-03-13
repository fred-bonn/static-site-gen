import unittest

from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestNodeSplitter(unittest.TestCase):
    def test_split_nodes(self):
        nodes = [TextNode("This is a **bold** node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ])

    def test_split_nodes_multiple(self):
        nodes = [TextNode("This is a **bold** and **another bold** node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ])

    def test_split_nodes_mixed_delimiters(self):
        nodes = [TextNode("This is a **bold** and _italic_ node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
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
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a bold node", TextType.TEXT)
        ])

    def test_split_nodes_unmatched_delimiter(self):
        nodes = [TextNode("This is a **bold node", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertTrue("missing closing deliminiter" in str(context.exception))

    def test_split_nodes_non_text_node(self):
        nodes = [TextNode("This is a bold node", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a bold node", TextType.BOLD)
        ])

    def test_split_nodes_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_split_nodes_delimiter_at_edge(self):
        nodes = [TextNode("This is **bold at edge**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold at edge", TextType.BOLD)
        ])

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is an image ![alt](image.jpg) in markdown"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt", "image.jpg")])

    def test_extract_markdown_links(self):
        text = "This is a link [anchor](https://example.com) in markdown"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("anchor", "https://example.com")])

    def test_extract_markdown_links_no_image(self):
        text = "This is a link [anchor](https://example.com) and an image ![alt](image.jpg)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("anchor", "https://example.com")])

    def test_extract_markdown_images_no_link(self):
        text = "This is an image ![alt](image.jpg) and a link [anchor](https://example.com)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt", "image.jpg")])

    def test_extract_markdown_links_no_markdown(self):
        text = "This is a link and an image in markdown"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_images_no_markdown(self):
        text = "This is a link and an image in markdown"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_links_image(self):
        text = "This is not a link ![image](image.jpg)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_images_link(self):
        text = "This is not an image [link](link)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_links_multiple(self):
        text = "This is a link [link1](https://example.com) and another link [link2](https://example.org)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link1", "https://example.com"), ("link2", "https://example.org")])

    def test_extract_markdown_images_multiple(self):
        text = "This is an image ![alt1](image1.jpg) and another image ![alt2](image2.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt1", "image1.jpg"), ("alt2", "image2.jpg")])

    def test_extract_markdown_links_malformed(self):
        text = "This is a malformed link [anchor](https://example.com"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_images_malformed(self):
        text = "This is a malformed image ![alt(image.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

class TestMarkdownSplitting(unittest.TestCase):
    def test_split_nodes_image(self):
        nodes = [TextNode("This is an image ![alt](image.jpg) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image.jpg"),
            TextNode(" in markdown", TextType.TEXT)
        ])

    def test_split_nodes_link(self):
        nodes = [TextNode("This is a link [anchor](https://example.com) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes, [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("anchor", TextType.LINK, "https://example.com"),
            TextNode(" in markdown", TextType.TEXT)
        ])

    def test_split_nodes_image_and_link(self):
        nodes = [TextNode("This is an image ![alt](image.jpg) and a link [anchor](https://example.com) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_link(split_nodes_image(nodes))
        self.assertEqual(new_nodes, [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image.jpg"),
            TextNode(" and a link ", TextType.TEXT),
            TextNode("anchor", TextType.LINK, "https://example.com"),
            TextNode(" in markdown", TextType.TEXT)
        ])

    def test_split_nodes_no_markdown(self):
        nodes = [TextNode("This is a link and an image in markdown", TextType.TEXT)]
        new_nodes = split_nodes_link(split_nodes_image(nodes))
        self.assertEqual(new_nodes, [
            TextNode("This is a link and an image in markdown", TextType.TEXT)
        ])

    def test_split_nodes_malformed_markdown(self):
        nodes = [TextNode("This is a malformed link [anchor](https://example.com and a malformed image ![alt(image.jpg)", TextType.TEXT)]
        new_nodes = split_nodes_link(split_nodes_image(nodes))
        self.assertEqual(new_nodes, [
            TextNode("This is a malformed link [anchor](https://example.com and a malformed image ![alt(image.jpg)", TextType.TEXT)
        ])

    def test_split_nodes_non_text_node(self):
        nodes = [TextNode("anchor", TextType.LINK, "https://example.com")]
        new_nodes = split_nodes_link(split_nodes_image(nodes))
        self.assertEqual(new_nodes, [
            TextNode("anchor", TextType.LINK, "https://example.com")
        ])

    def test_split_nodes_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [])

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is a text node"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode(text, TextType.TEXT)])

    def test_text_to_textnodes_bold_italic_code(self):
        text = "This is a **bold** and _italic_ and `code` node"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" node", TextType.TEXT)
        ])

if __name__ == "__main__":
    unittest.main()
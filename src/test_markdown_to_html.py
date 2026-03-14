import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## **Bold Heading** 2
test

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><p>## <b>Bold Heading</b> 2 test</p><h3>Heading 3</h3></div>",
        )

    def test_quote_malformed(self):
        md = """
> This is a quote
>
> that spans multiple lines
>test
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\n\nthat spans multiple lines\ntest</blockquote></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> that spans multiple lines
> test
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nthat spans multiple lines\ntest</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- **Bold Item** 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li><b>Bold Item</b> 3</li></ul></div>",
        )

def test_ordered_list(self):
        md = """
1. Item 1
2. _Italic Item_ 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li><i>Italic Item</i> 2</li><li>Item 3</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
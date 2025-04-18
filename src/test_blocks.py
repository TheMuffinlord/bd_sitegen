import unittest

from textnode import *
from loosefunctions import *
from blockfuncs import *

if __name__ == "__main__":
    unittest.main()

class TestBlocks(unittest.TestCase):
    def test_block_types_1(self):
        block = "# this is a header block"
        test_case = block_to_block_type(block)
        self.assertEqual(BlockType.heading, test_case)

    def test_block_types_2(self): #bad formatting for header
        block1 = "#####this is not a header block"
        test_case = block_to_block_type(block1)
        self.assertEqual(BlockType.paragraph, test_case)

    def test_block_types_ol(self): #ordered list
        block = """
        1. this is a block!
        2. this is still a block!
        3. this will be a block!"""
        test_case = block_to_block_type(block)
        self.assertEqual(BlockType.ordered_list, test_case)

    def test_block_types_ol2(self):
        block = """
        1. this is the start of a list
            2. this is the next in a list
            3. this is the third in a list
            99. this should probably break the list but won't because ordered list logic isn't in there yet"""
        test_case = block_to_block_type(block)
        self.assertNotEqual(BlockType.ordered_list, test_case)
    
    def test_block_types_code1(self):
        block = """```
        here is a block of code
        ```"""
        test_case = block_to_block_type(block)
        self.assertEqual(BlockType.code, test_case)

    def test_block_types_code2(self): #improper code format
        b = """```
        this should not be a block of code"""
        test_case = block_to_block_type(b)
        self.assertEqual(BlockType.paragraph, test_case)

    def test_block_types_quote(self):
        b = """> be me
        > be programming test cases
        > have to pee
        > mfw"""
        test_case = block_to_block_type(b)
        self.assertEqual(BlockType.quote, test_case)

    def test_html_blocks_1(self):
        bigblock = """
# here's a header with some _italics_ and **bold text** in it
"""
        test_case = markdown_to_html_node(bigblock)
        test_html = test_case.to_html()
        self.assertEqual(
            test_html,
            "<div><h1>here's a header with some <i>italics</i> and <b>bold text</b> in it</h1></div>"
        )
    
    def test_html_blocks_2(self):
        bigblock = """
> be me
> _writing in italics_
> hoping this works"""
        test = markdown_to_html_node(bigblock)
        test_html = test.to_html()
        self.assertEqual(
            test_html,
            "<div><blockquote>be me\n<i>writing in italics</i>\nhoping this works</blockquote></div>"
        )

    def test_html_blocks_3(self): #unsorted list
        ul_text = """
- an unsorted list
- an _impromptu_ poem **appears**
- i'm getting hungry"""
        t_block = markdown_to_html_node(ul_text)
        test_html = t_block.to_html()
        self.assertEqual(
            test_html,
            "<div><ul><li>an unsorted list</li><li>an <i>impromptu</i> poem <b>appears</b></li><li>i'm getting hungry</li></ul></div>"
        )
    
    def test_html_blocks_4(self): #ordered list!
        ol_text = """
1. i should have gotten a snack
2. now it's getting late
3. it'll be dinner time soon :("""
        t_nodes = markdown_to_html_node(ol_text)
        test_html = t_nodes.to_html()
        self.assertEqual(
            test_html,
            "<div><ol><li>i should have gotten a snack</li><li>now it's getting late</li><li>it'll be dinner time soon :(</li></ol></div>"
        )

    def test_html_blocks_5(self): #code blocks
        cb_text = """
``` this is a code block
the whole thing is a code block
until i end it
``` """
        cb_nodes = markdown_to_html_node(cb_text)
        test_html = cb_nodes.to_html()
        #print(test_html)
        self.assertEqual(
            test_html,
            "<div><pre><code>this is a code block\nthe whole thing is a code block\nuntil i end it</code></pre></div>"
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
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
        #print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
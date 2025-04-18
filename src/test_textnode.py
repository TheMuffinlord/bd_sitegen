import unittest

from textnode import *
from loosefunctions import *
from blockfuncs import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_type(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        node2 = TextNode("this is a bold node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_noteq_text(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        node2 = TextNode("this is an italics node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("this node has a url", TextType.LINK, "https://minimumviable.website")
        node2 = TextNode("this node has a url", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_text2html_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_t2h_2(self):
        tnode = TextNode("a picture of a dog", TextType.IMAGE, "buddy.jpeg")
        hnode = text_node_to_html_node(tnode)
        self.assertEqual(hnode.tag, "img")
        self.assertEqual(hnode.props["alt"], "a picture of a dog")
        self.assertEqual(hnode.value, None)

    def test_node_split_1(self):
        oldnode = TextNode("this is a `code block` of text", TextType.TEXT)
        newnode = split_nodes_delimiter([oldnode], "`", TextType.CODE)
        result = [
            TextNode("this is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" of text", TextType.TEXT)
        ]
        self.assertEqual(newnode, result)

    def test_node_split_2(self): #expect an error
        node1 = TextNode("this is a block of *plain text", TextType.BOLD)
        self.assertRaises(Exception, split_nodes_delimiter, [node1], "*", TextType.CODE) 
        #this took longer to figure out than the actual function!

    def test_node_split_just_text(self):
        node1 = TextNode("this is just a block of plain text but **i threw some bold in there** to see if it parses", TextType.BOLD)
        node2 = split_nodes_delimiter([node1], "**", TextType.ITALIC)
        self.assertEqual([node1], node2)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extracting_links(self):
        matches = extract_markdown_links("[click here](https://minimumviable.website) for a cool website")
        self.assertListEqual([("click here", "https://minimumviable.website")], matches)

    def test_extracting_multiple(self):
        img_match = extract_markdown_images("this is an image of ![an image of a duck](https://duck.website.jpeg)")
        link_match = extract_markdown_links("this is a link to [an image of a duck](https://duck.website.jpeg)")
        self.assertListEqual(img_match, link_match)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_2(self): #one image with no text on either side
        node = TextNode("![here is an image](image.jpeg)", TextType.TEXT)
        test_case = split_nodes_image([node])
        self.assertListEqual([TextNode("here is an image", TextType.IMAGE, "image.jpeg")], test_case)

    def test_split_images_3(self): #one image but there's also a link on there, text on all sides
        node = TextNode(
            "here is a block of text ![with an image](image.jpeg) and with a [link](link.html) on the side of it.",
            TextType.TEXT,
        )
        test_case = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("here is a block of text ", TextType.TEXT),
                TextNode("with an image", TextType.IMAGE, "image.jpeg"),
                TextNode(" and with a [link](link.html) on the side of it.", TextType.TEXT),
            ],
            test_case,
        )

    def test_split_links_1(self): #same test as above but for links this time
        node = TextNode(
            "here is a block of text ![with an image](image.jpeg) and with a [link](link.html) on the side of it.",
            TextType.TEXT,
        )
        test_case = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("here is a block of text ![with an image](image.jpeg) and with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link.html"),
                TextNode(" on the side of it.", TextType.TEXT),
            ],
            test_case,
        )

    def test_split_links_2(self): #no link or image
        node = TextNode("here's a block of text with no links or images", TextType.TEXT)
        test_case = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("here's a block of text with no links or images", TextType.TEXT),
            ],
            test_case
        )

    def test_split_images_4(self): #two nodes as input
        node = TextNode("here's an image: ![a duck](duck.jpeg)", TextType.TEXT)
        node2 = TextNode("a second image: ![duck2](duck2.jpeg)", TextType.TEXT)
        test_case = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("here's an image: ", TextType.TEXT),
                TextNode("a duck", TextType.IMAGE, "duck.jpeg"),
                TextNode("a second image: ", TextType.TEXT),
                TextNode("duck2", TextType.IMAGE, "duck2.jpeg"),
            ],
            test_case
        )

    def test_text_splitter_1(self): #provided test case
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        #node = TextNode(text, TextType.TEXT)
        test_case = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            test_case
        )

    def test_text_splitter_2(self): #how many of these do i gotta writeeeeeeeeeeeeeeee
        text = "_look_, I'm getting **tired**. `how many of these should i write?`"
        test_case = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("look", TextType.ITALIC),
                TextNode(", I'm getting ", TextType.TEXT),
                TextNode("tired", TextType.BOLD),
                TextNode(". ", TextType.TEXT),
                TextNode("how many of these should i write?", TextType.CODE)
            ],
            test_case
        )

    def test_text_splitter_3(self): #an underscore in the image tag. let's see if it catches it
        text = "okay, have this ![real image](image_1.url) _real_ image."
        test_case = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("okay, have this ", TextType.TEXT),
                TextNode("real image", TextType.IMAGE, "image_1.url"),
                TextNode(" ", TextType.TEXT),
                TextNode("real", TextType.ITALIC),
                TextNode(" image.", TextType.TEXT),
            ],
            test_case
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""" #i hate how this breaks formatting ugh
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
oh god how did this get here i am not good with computer
"""
        test_case = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "oh god how did this get here i am not good with computer",
            ],
            test_case
        )

    def test_markdown_to_blocks_3(self):
        md = """
it's real stupid how python respects tabs so much
but there's no way to strip them from a block of text without regexes?

sucks bro
"""
        test_case = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "it's real stupid how python respects tabs so much\nbut there's no way to strip them from a block of text without regexes?",
                "sucks bro",
            ],
            test_case
        )



#ok just make sure this is at the bottom        
if __name__ == "__main__":
    unittest.main()
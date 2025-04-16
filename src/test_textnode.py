import unittest

from textnode import *

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

if __name__ == "__main__":
    unittest.main()
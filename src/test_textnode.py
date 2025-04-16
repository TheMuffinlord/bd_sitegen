import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_type(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        node2 = TextNode("this is a bold node", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_noteq_text(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        node2 = TextNode("this is an italics node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("this node has a url", TextType.LINK, "https://minimumviable.website")
        node2 = TextNode("this node has a url", TextType.LINK, None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
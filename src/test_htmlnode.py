import unittest

from htmlnode import *

class TestHMTLNode(unittest.TestCase):
    def test_basic(self):
        node1 = HTMLNode("p", "this is a test paragraph", None, {"style":"font-size: 12px", "width": "100%"})
        node2 = "HTMLNode(p, this is a test paragraph, None, {'style': 'font-size: 12px', 'width': '100%'})"
        node3 = str(node1)
        self.assertEqual(node3, node2)
    
    def test_props(self):
        node1 = HTMLNode("a", "click here to go to a cool website", None, {"href": "https://minimumviable.website", "target": "_blank"})
        node1a = node1.props_to_html()
        node2 = ' href="https://minimumviable.website" target="_blank"'
        self.assertEqual(node1a, node2)

    def test_none(self):
        node1 = HTMLNode()
        node2 = 'HTMLNode(None, None, None, None)'
        node1a = str(node1)
        self.assertEqual(node1a, node2)

    def test_leaf1(self):
        leaf1 = LeafNode("p", "here's a paragraph!")
        leaf2 = "<p>here's a paragraph!</p>"
        self.assertEqual(leaf1.to_html(), leaf2)

    def test_leaf2(self):
        leaf1 = LeafNode("a", "click this link!", {"href": "https://minimumviable.website"})
        leaf2 = '<a href="https://minimumviable.website">click this link!</a>'
        self.assertEqual(leaf1.to_html(), leaf2)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_noteq_parents(self):
        cn_1 = LeafNode("td", "table")
        cn_2 = LeafNode("td", "item2")
        pn_1 = LeafNode("tr", [cn_1, cn_2])
        pn_2 = LeafNode("tr", [cn_2, cn_1])
        self.assertNotEqual(pn_1, pn_2)

if __name__ == "__main__":
    unittest.main()
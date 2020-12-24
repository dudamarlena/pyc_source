# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gumbo/gumboc_test.py
# Compiled at: 2015-04-30 22:50:43
"""Tests for Gumbo CTypes bindings."""
__author__ = 'jdtang@google.com (Jonathan Tang)'
import StringIO, unittest, gumboc

class CtypesTest(unittest.TestCase):

    def testWordParse(self):
        with gumboc.parse('Test') as (output):
            doctype_node = output.contents.document.contents
            self.assertEquals(gumboc.NodeType.DOCUMENT, doctype_node.type)
            document = doctype_node.v.document
            self.assertEquals('', document.name)
            self.assertEquals('', document.public_identifier)
            self.assertEquals('', document.system_identifier)
            root = output.contents.root.contents
            self.assertEquals(gumboc.NodeType.ELEMENT, root.type)
            self.assertEquals(gumboc.Tag.HTML, root.tag)
            self.assertEquals(gumboc.Namespace.HTML, root.tag_namespace)
            self.assertEquals(2, len(root.children))
            head = root.children[0]
            self.assertEquals(gumboc.NodeType.ELEMENT, head.type)
            self.assertEquals(gumboc.Tag.HEAD, head.tag)
            self.assertEquals('head', head.tag_name)
            self.assertEquals(gumboc.Namespace.HTML, head.tag_namespace)
            self.assertEquals(0, len(head.original_tag))
            self.assertEquals('', str(head.original_end_tag))
            self.assertEquals(0, head.children.length)
            body = root.children[1]
            self.assertNotEquals(body, doctype_node)
            self.assertEquals(gumboc.NodeType.ELEMENT, body.type)
            self.assertEquals(gumboc.Tag.BODY, body.tag)
            self.assertEquals('body', body.tag_name)
            self.assertEquals(1, len(body.children))
            text_node = body.children[0]
            self.assertEquals(gumboc.NodeType.TEXT, text_node.type)
            self.assertEquals('Test', text_node.text)

    def testBufferThatGoesAway(self):
        for i in range(10):
            source = StringIO.StringIO('<foo bar=quux>1<p>2</foo>')
            parse_tree = gumboc.parse(source.read())
            source.close()

        with parse_tree as (output):
            root = output.contents.root.contents
            body = root.children[1]
            foo = body.children[0]
            self.assertEquals(gumboc.NodeType.ELEMENT, foo.type)
            self.assertEquals(gumboc.Tag.UNKNOWN, foo.tag)
            self.assertEquals('<foo bar=quux>', str(foo.original_tag))
            self.assertEquals('', str(foo.original_end_tag))
            self.assertEquals('foo', foo.tag_name.decode('utf-8'))
            self.assertEquals('bar', foo.attributes[0].name)
            self.assertEquals('quux', foo.attributes[0].value)

    def testUnknownTag(self):
        with gumboc.parse('<foo bar=quux>1<p>2</foo>') as (output):
            root = output.contents.root.contents
            body = root.children[1]
            foo = body.children[0]
            self.assertEquals(gumboc.NodeType.ELEMENT, foo.type)
            self.assertEquals(gumboc.Tag.UNKNOWN, foo.tag)
            self.assertEquals('<foo bar=quux>', str(foo.original_tag))
            self.assertEquals('', str(foo.original_end_tag))
            self.assertEquals('foo', foo.tag_name.decode('utf-8'))
            self.assertEquals('bar', foo.attributes[0].name)
            self.assertEquals('quux', foo.attributes[0].value)

    def testSarcasm(self):
        with gumboc.parse('<div><sarcasm><div></div></sarcasm></div>') as (output):
            root = output.contents.root.contents
            body = root.children[1]
            div = body.children[0]
            sarcasm = div.children[0]
            self.assertEquals(gumboc.NodeType.ELEMENT, sarcasm.type)
            self.assertEquals(gumboc.Tag.UNKNOWN, sarcasm.tag)
            self.assertEquals('<sarcasm>', str(sarcasm.original_tag))
            self.assertEquals('</sarcasm>', str(sarcasm.original_end_tag))
            self.assertEquals('sarcasm', sarcasm.tag_name.decode('utf-8'))

    def testEnums(self):
        self.assertEquals(gumboc.Tag.A, gumboc.Tag.A)
        self.assertEquals(hash(gumboc.Tag.A.value), hash(gumboc.Tag.A))

    def testFragment(self):
        with gumboc.parse('<div></div>', fragment_context=gumboc.Tag.TITLE, fragment_namespace=gumboc.Namespace.SVG) as (output):
            root = output.contents.root.contents
            self.assertEquals(1, len(root.children))
            div = root.children[0]
            self.assertEquals(gumboc.NodeType.ELEMENT, div.type)
            self.assertEquals(gumboc.Tag.DIV, div.tag)
            self.assertEquals(gumboc.Namespace.HTML, div.tag_namespace)


if __name__ == '__main__':
    unittest.main()
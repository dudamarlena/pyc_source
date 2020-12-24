# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/test_nodetree.py
# Compiled at: 2008-07-24 14:48:01
import unittest
from zope.interface.verify import verifyObject

class NodeTreeTests(unittest.TestCase):

    def setUp(self):
        from twiddler import Twiddler
        t = Twiddler('<?xml version=\'1.0\' encoding=\'utf-8\'?><moo><cow id="test">some text</cow>tail</moo>')
        self.t = t.node
        self.n = t['test'].node

    def test_node_interface(self):
        from twiddler.interfaces import INode
        verifyObject(INode, self.n)

    def test_node_attributetypes(self):
        self.failUnless(isinstance(self.n.tag, unicode))
        self.failUnless(isinstance(self.n.text, unicode))
        self.failUnless(isinstance(self.n.tail, unicode))

    def test_tree_interface(self):
        from twiddler.interfaces import ITree
        verifyObject(ITree, self.t)

    def test_bad_element_search(self):
        self.assertRaises(KeyError, self.n.search, 'foo')


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(NodeTreeTests),))
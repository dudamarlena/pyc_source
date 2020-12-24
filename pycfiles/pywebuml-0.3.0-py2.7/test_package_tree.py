# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\tests\test_package_tree.py
# Compiled at: 2011-02-03 18:18:28
"""
Some basic tests fort the ``pywebum.package_tree.TreeNode``
"""
from unittest2 import TestCase
from pywebuml.package_tree import TreeNode

class TestTreeNode(TestCase):

    def setUp(self):
        self.tree = TreeNode('', '')

    def test_create_sub_tree(self):
        self.tree.add_child('global.A')
        self.tree.add_child('global.B')
        self.tree.add_child('global.C.D')
        self.tree.add_child('foo')
        self.assertEquals(len(self.tree.childs), 2)
        self.assertEquals(self.tree.childs[0].name, 'global')
        self.assertEquals(self.tree.childs[1].name, 'foo')
        self.assertEquals(len(self.tree.childs[0].childs), 3)
        self.assertEquals(self.tree.childs[0].childs[0].name, 'C')
        self.assertEquals(self.tree.childs[0].childs[1].name, 'A')
        self.assertEquals(self.tree.childs[0].childs[2].name, 'B')
        self.assertEquals(self.tree.childs[0].childs[0].childs[0].name, 'D')
        self.assertIsNot(self.tree.get('global'), None)
        self.assertIsNot(self.tree.get('global.A', True), None)
        self.assertIsNot(self.tree.get('global.B', True), None)
        self.assertIsNot(self.tree.get('global.C', True), None)
        self.assertIsNot(self.tree.get('global.C.D', True), None)
        self.assertIsNot(self.tree.get('foo', True), None)
        self.assertIs(self.tree.get('DOESNT_EXISTS', True), None)
        return
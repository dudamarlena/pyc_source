# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cor/bin/src/crystal_torture/tests/test_node.py
# Compiled at: 2018-07-19 04:18:07
import unittest
from crystal_torture import Node

class NodeTestCase(unittest.TestCase):
    """Test for Site Class"""

    def setUp(self):
        self.index = 1
        self.element = 'Mg'
        self.labels = {1: 'A', 2: str(self.index)}
        self.neighbours_ind = [1, 2, 9, 10]
        self.node = Node(self.index, self.element, self.labels, self.neighbours_ind)

    def test_node_is_initialised(self):
        self.assertEqual(self.node.index, self.index)
        self.assertEqual(self.node.element, self.element)
        self.assertEqual(self.node.labels, self.labels)
        self.assertEqual(self.node.neighbours_ind, self.neighbours_ind)


if __name__ == '__main__':
    unittest.main()
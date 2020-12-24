# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/tests/test_node.py
# Compiled at: 2018-05-29 04:04:22
# Size of source mod 2**32: 731 bytes
import unittest
from crystal_torture import Node

class NodeTestCase(unittest.TestCase):
    """NodeTestCase"""

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
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_gcounter.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 1802 bytes
import unittest, uuid, set_sys_path
from gcounter import GCounter
from node import Node

class TestGCounter(unittest.TestCase):

    def setUp(self):
        self.node1 = Node(uuid.uuid4())
        self.node2 = Node(uuid.uuid4())
        self.gc1 = GCounter(uuid.uuid4())
        self.gc1.add_new_node(self.node1.id)
        self.gc1.add_new_node(self.node2.id)
        self.gc2 = GCounter(uuid.uuid4())
        self.gc2.add_new_node(self.node1.id)
        self.gc2.add_new_node(self.node2.id)
        self.gc1.inc(self.node1.id)
        self.gc1.inc(self.node1.id)
        self.gc1.inc(self.node2.id)
        self.gc2.inc(self.node1.id)
        self.gc2.inc(self.node2.id)
        self.gc2.inc(self.node2.id)
        self.gc2.inc(self.node2.id)

    def test_check_increment(self):
        self.assertEqual(self.gc1.payload[self.node1.id], 2)
        self.assertEqual(self.gc1.payload[self.node2.id], 1)
        self.assertEqual(self.gc2.payload[self.node1.id], 1)
        self.assertEqual(self.gc2.payload[self.node2.id], 3)

    def test_merging_gcounters(self):
        self.gc2.merge(self.gc1)
        self.assertEqual(self.gc2.payload[self.node1.id], 2)
        self.assertEqual(self.gc2.payload[self.node2.id], 3)
        self.gc1.merge(self.gc2)
        self.assertEqual(self.gc1.payload[self.node1.id], 2)
        self.assertEqual(self.gc1.payload[self.node2.id], 3)
        self.assertEqual(self.gc1.payload, self.gc2.payload)


if __name__ == '__main__':
    unittest.main()
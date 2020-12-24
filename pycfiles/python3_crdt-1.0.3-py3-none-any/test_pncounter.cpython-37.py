# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gg/PycharmProjects/gg-python3-crdt/build/lib/tests/test_pncounter.py
# Compiled at: 2019-04-22 02:28:32
# Size of source mod 2**32: 1820 bytes
import unittest, uuid, set_sys_path
from pncounter import PNCounter
from node import Node

class TestPNCounter(unittest.TestCase):

    def setUp(self):
        self.node1 = Node(uuid.uuid4())
        self.node2 = Node(uuid.uuid4())
        self.pn1 = PNCounter(uuid.uuid4())
        self.pn1.add_new_node(self.node1.id)
        self.pn1.add_new_node(self.node2.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node2.id)
        self.pn1.inc(self.node2.id)
        self.pn1.inc(self.node2.id)
        self.pn1.dec(self.node1.id)
        self.pn1.dec(self.node1.id)
        self.pn1.dec(self.node1.id)
        self.pn1.dec(self.node2.id)
        self.pn2 = PNCounter(uuid.uuid4())
        self.pn2.add_new_node(self.node1.id)
        self.pn2.add_new_node(self.node2.id)
        self.pn2.inc(self.node1.id)
        self.pn2.inc(self.node2.id)
        self.pn2.inc(self.node2.id)
        self.pn2.inc(self.node2.id)
        self.pn2.dec(self.node1.id)
        self.pn2.dec(self.node2.id)
        self.pn2.dec(self.node2.id)

    def test_merge(self):
        self.pn1.display('pn1')
        self.pn2.display('pn2')
        self.pn2.merge(self.pn1)
        self.pn1.merge(self.pn2)
        self.assertEqual(self.pn1.query(), self.pn2.query())


if __name__ == '__main__':
    unittest.main()
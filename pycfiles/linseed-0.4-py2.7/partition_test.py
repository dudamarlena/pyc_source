# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/test/partition_test.py
# Compiled at: 2012-02-12 10:18:51
import unittest
from linseed import Partition, Partitions

class PartitionsTest(unittest.TestCase):

    def setUp(self):
        self.p = Partitions()

    def test_partitions(self):
        for p in self.p.partitions:
            self.assertTrue(isinstance(p, Partition))

    def test_iterate(self):
        for p in self.p:
            self.assertTrue(isinstance(p, Partition))


class PartitionTest(unittest.TestCase):

    def setUp(self):
        self.p = Partitions()

    def test_device(self):
        for p in self.p:
            p.device

    def test_mount_point(self):
        for p in self.p:
            p.device

    def test_type(self):
        for p in self.p:
            p.type

    def test_usage(self):
        for p in self.p:
            self.assertTrue(p.usage.total >= 0)
            self.assertTrue(p.usage.used >= 0)
            self.assertTrue(p.usage.used <= p.usage.total)
            self.assertTrue(p.usage.free >= 0)
            self.assertTrue(p.usage.free <= p.usage.total)
            self.assertTrue(p.usage.percent >= 0)
            self.assertTrue(p.usage.percent <= 100)
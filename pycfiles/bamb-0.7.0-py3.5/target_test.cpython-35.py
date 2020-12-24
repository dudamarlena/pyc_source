# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/target_test.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 1180 bytes
import unittest, domain.base
from domain import base

class Foo(base.EasySerializable, base.ListTree):

    def __init__(self, name=''):
        self.name = name
        base.EasySerializable.__init__(self)
        base.ListTree.__init__(self)


class TargetTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        f = self.build_object()
        d = f.es_to_dict()
        self.assertTrue(len(d) > 0)
        print(d)
        f1 = base.EasySerializable.es_load(d)
        self.assertTrue(isinstance(f1, domain.base.Target))

    def build_object(self):
        t = domain.base.Target(name='test scope')
        t1 = domain.base.Target(name='cluster 1')
        t2 = domain.base.Target(name='cluster 2')
        t1.lt_extend_children([domain.base.Target(ip='192.168.1.1', name='host1-1'), domain.base.Target(ip='192.168.1.2', name='host1-2'), domain.base.Target(ip='192.168.1.3', name='host1-3')])
        t2.lt_extend_children([domain.base.Target(ip='192.168.2.1', name='host2-1'), domain.base.Target(ip='192.168.2.2', name='host2-2')])
        t.lt_extend_children([t1, t2])
        return t
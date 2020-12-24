# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/tests/test_pools.py
# Compiled at: 2006-08-16 19:11:48
import unittest
from zope.interface.verify import verifyClass, verifyObject
from evogrid.interfaces import IPool
from evogrid.common.replicators import Replicator
from evogrid.common.pools import Pool, OrderedPool, UnionPool

class AbstractPoolTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.pool = self.klass()
        self.replicators = [ Replicator(cs=i) for i in range(10) ]

    def test_interface(self):
        self.assert_(verifyClass(IPool, self.klass))
        self.assert_(verifyObject(IPool, self.pool))

    def test_add_and_len(self):
        pool = self.pool
        for rep in self.replicators:
            pool.add(rep)

        self.assertEquals(len(pool), 10)

    def test_add_and_contains(self):
        for rep in self.replicators:
            self.pool.add(rep)

        for rep in self.replicators:
            self.assert_(rep in self.pool)

    def test_iterable_init(self):
        pool = self.klass(self.replicators)
        self.assertEquals(len(self.replicators), len(pool))
        for rep in self.replicators:
            self.assert_(rep in pool)

    def test_pop(self):
        pool = self.pool
        rep = Replicator()
        pool.add(rep)
        self.assertEquals(len(pool), 1)
        rep2 = pool.pop()
        self.assertEquals(len(pool), 0)
        self.assertEquals(rep, rep2)
        self.assertRaises(ValueError, pool.pop)

    def test_remove(self):
        pool = self.pool
        rep = Replicator(cs='some cs')
        rep2 = Replicator(cs='some cs 2')
        pool.add(rep)
        pool.add(rep2)
        self.assertEquals(len(pool), 2)
        self.assert_(rep in pool)
        self.assert_(rep2 in pool)
        self.assertRaises(ValueError, pool.remove, Replicator(cs='some cs 2'))
        self.assertEquals(len(pool), 2)
        self.assert_(rep in pool)
        self.assert_(rep2 in pool)
        pool.remove(rep)
        self.assertEquals(len(pool), 1)
        self.assert_(rep not in pool)
        self.assert_(rep2 in pool)
        pool.remove(rep2)
        self.assertEquals(len(pool), 0)
        self.assert_(rep not in pool)
        self.assert_(rep2 not in pool)
        self.assertRaises(ValueError, pool.remove, rep2)

    def test_clear(self):
        pool = self.pool
        for rep in self.replicators:
            pool.add(rep)

        self.assertEquals(len(pool), len(self.replicators))
        pool.clear()
        self.assertEquals(len(pool), 0)
        for rep in self.replicators:
            self.assert_(rep not in pool)

    def test_iter(self):
        pool = self.pool
        for rep in self.replicators:
            pool.add(rep)

        for rep in pool:
            self.assert_(rep in self.replicators)

        for (i, rep) in enumerate(pool):
            self.assert_(rep in self.replicators)

        self.assertEquals(i + 1, len(self.replicators))


class PoolTestCase(AbstractPoolTestCase):
    __module__ = __name__
    klass = Pool

    def test_repr(self):
        pool = self.pool
        pool.add(Replicator(cs=1))
        self.assertEquals(pool.__repr__(), 'Pool([Replicator(cs=1)])')


class OrderedPoolTestCase(AbstractPoolTestCase):
    __module__ = __name__
    klass = OrderedPool

    def test_repr(self):
        pool = self.pool
        pool.add(Replicator(cs=1))
        self.assertEquals(pool.__repr__(), 'OrderedPool([Replicator(cs=1)])')

    def test_order(self):
        pool = self.klass(self.replicators)
        for (rep1, rep2) in zip(pool, self.replicators):
            self.assertEquals(rep1, rep2)


class UnionPoolTestCase(AbstractPoolTestCase):
    __module__ = __name__
    klass = UnionPool

    def setUp(self):
        pool1 = Pool()
        pool2 = OrderedPool()
        self.pool = UnionPool((pool1, pool2))
        self.replicators = [ Replicator(cs=i) for i in range(10) ]

    def test_repr(self):
        pool = self.pool
        pool.add(Replicator(cs=1))
        self.assertEquals(pool.__repr__(), 'UnionPool([Pool([]), OrderedPool([Replicator(cs=1)])])')

    def test_iterable_init(self):
        pass


del AbstractPoolTestCase

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(PoolTestCase))
    suite.addTests(unittest.makeSuite(OrderedPoolTestCase))
    suite.addTests(unittest.makeSuite(UnionPoolTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
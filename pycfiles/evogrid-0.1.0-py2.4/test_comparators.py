# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/tests/test_comparators.py
# Compiled at: 2006-05-14 12:56:47
import unittest
from zope.interface.verify import verifyClass, verifyObject
from evogrid.common.comparators import SimpleComparator
from evogrid.interfaces import IComparator

class FakeEvaluatedReplicator:
    __module__ = __name__

    def __init__(self, ev=0):
        self.evaluation = ev

    def __repr__(self):
        return '<%s object with evaluation=%r>' % (self.__class__.__name__, self.evaluation)


class ComparatorTestCase(unittest.TestCase):
    __module__ = __name__

    def test_interfaces(self):
        self.assert_(verifyClass(IComparator, SimpleComparator))

    def test_SimpleComparator(self):
        simple_comparator = SimpleComparator()
        self.assert_(verifyObject(IComparator, simple_comparator))
        rep1, rep2 = FakeEvaluatedReplicator(1), FakeEvaluatedReplicator(2)
        self.assertEquals(simple_comparator.cmp(rep1, rep2), -1)
        self.assertEquals(simple_comparator.cmp(rep1, rep1), 0)
        self.assertEquals(simple_comparator.cmp(rep2, rep2), 0)
        self.assertEquals(simple_comparator.cmp(rep2, rep1), 1)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ComparatorTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
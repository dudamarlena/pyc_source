# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/QueueCatalog/tests/test_CatalogEventQueueSet.py
# Compiled at: 2008-05-13 06:38:01
from __future__ import generators
import unittest
from Acquisition import aq_base
from Products.QueueCatalog.CatalogEventQueue import ADDED
from Products.QueueCatalog.CatalogEventQueue import CHANGED
from Products.QueueCatalog.CatalogEventQueue import CHANGED_ADDED
from Products.QueueCatalog.CatalogEventQueue import REMOVED

def eratosthenes():
    """Yields the sequence of prime numbers via the Sieve of Eratosthenes."""
    D = {}
    q = 2
    while 1:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)

            del D[q]
        q += 1


def _isPrime(count):
    """ Alternate implementation, using Sieve.
    """
    assert type(count) is type(0)
    for prime in eratosthenes():
        if prime == count:
            return 1
        if prime > count:
            return 0


class CatalogEventQueueSetTests(unittest.TestCase):
    __module__ = __name__

    def _getTargetClass(self):
        from Products.QueueCatalog.CatalogEventQueueSet import CatalogEventQueueSet
        return CatalogEventQueueSet

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeDelegate(self):
        from Products.QueueCatalog.CatalogEventQueueSet import ICatalogEventQueueSetDelegate

        class DummyCatalogEventQueueSetDelegate:
            __module__ = __name__
            __implements__ = (
             ICatalogEventQueueSetDelegate,)

            def __init__(self):
                self._uids = {}

            def hasUID(self, uid):
                return self._uids.get(uid) is not None

            def add(self, uid):
                if self._uids.get(uid) is not None:
                    raise AssertionError, 'Duplicate'
                self._uids[uid] = 0
                return

            def change(self, uid):
                self._uids[uid] = self._uids.setdefault(uid, 0) + 1

            def remove(self, uid):
                try:
                    del self._uids[uid]
                except KeyError:
                    pass

            def getUIDCount(self, uid):
                return self._uids[uid]

        return DummyCatalogEventQueueSetDelegate()

    def test_ctor_default(self):
        set = self._makeOne()
        self.failUnless(_isPrime(set.getBucketCount()))
        self.assertEquals(set.getBucketCount(), len(set._queues))
        self.assertEquals(set.getDelegate(), None)
        events = [ x for x in set.listEvents() ]
        self.assertEquals(len(events), 0)
        return

    def test_ctor_explicit_delegate(self):
        delegate = self._makeDelegate()
        set = self._makeOne(delegate=delegate)
        self.failUnless(aq_base(set.getDelegate()) is delegate)

    def test_ctor_nonconforming_delegate(self):

        class NotDelegate:
            __module__ = __name__

        self.assertRaises(ValueError, self._makeOne, delegate=NotDelegate())

    def test_ctor_explicit_bucket_count(self):
        set = self._makeOne(bucket_count=11)
        self.assertEquals(set.getBucketCount(), 11)
        self.assertEquals(len(set._queues), 11)

    def test_ctor_bucket_count_not_prime(self):
        self.assertRaises(ValueError, self._makeOne, bucket_count=1008)

    def test_setDelegate(self):
        set = self._makeOne()
        delegate = self._makeDelegate()
        set.setDelegate(delegate)
        self.failUnless(aq_base(set.getDelegate()) is delegate)

    def test_setDelegate_nonconforming(self):

        class NotDelegate:
            __module__ = __name__

        set = self._makeOne()
        self.assertRaises(ValueError, set.setDelegate, NotDelegate())

    def test_setBucketCount(self):
        set = self._makeOne()
        set.setBucketCount(11)
        self.assertEquals(set.getBucketCount(), 11)
        self.assertEquals(len(set._queues), 11)

    def test_setBucketCount_non_prime(self):
        set = self._makeOne()
        self.assertRaises(ValueError, set.setBucketCount, 9)

    def test_update_non_event(self):
        set = self._makeOne()
        self.assertRaises(ValueError, set.update, 'foo', 42)

    def test_update(self):
        set = self._makeOne()
        set.update('foo', ADDED)
        events = [ x for x in set.listEvents() ]
        self.assertEquals(len(events), 1)
        (uid, event) = events[0]
        self.assertEqual(uid, 'foo')
        self.assertEqual(event, ADDED)

    def test_update_collapsing_add_change(self):
        set = self._makeOne()
        set.update('foo', ADDED)
        set.update('foo', CHANGED)
        events = [ x for x in set.listEvents() ]
        self.assertEquals(len(events), 1)
        (uid, event) = events[0]
        self.assertEqual(uid, 'foo')
        self.assertEqual(event, CHANGED_ADDED)

    def test_update_collapsing_add_change_remove(self):
        set = self._makeOne()
        set.update('bar', ADDED)
        set.update('bar', CHANGED)
        set.update('bar', REMOVED)
        events = [ x for x in set.listEvents() ]
        self.assertEquals(len(events), 1, events)
        (uid, event) = events[0]
        self.assertEqual(uid, 'bar')
        self.assertEqual(event, REMOVED)

    def test_update_remove_then_change(self):
        set = self._makeOne()
        set.update('bar', ADDED)
        set.update('bar', REMOVED)
        self.assertRaises(TypeError, set.update, 'bar', CHANGED)

    def test_process_add(self):
        delegate = self._makeDelegate()
        set = self._makeOne(delegate=delegate)
        self.failIf(delegate.hasUID('added'))
        set.update('added', ADDED)
        set.process()
        self.failUnless(delegate.hasUID('added'))
        self.assertEqual(delegate.getUIDCount('added'), 0)

    def test_process_change(self):
        delegate = self._makeDelegate()
        set = self._makeOne(delegate=delegate)
        self.failIf(delegate.hasUID('changed'))
        set.update('changed', CHANGED)
        set.update('changed', CHANGED)
        set.update('changed', CHANGED)
        set.process()
        self.failUnless(delegate.hasUID('changed'))
        self.assertEqual(delegate.getUIDCount('changed'), 1)

    def test_process_add_and_change(self):
        delegate = self._makeDelegate()
        set = self._makeOne(delegate=delegate)
        self.failIf(delegate.hasUID('added_changed'))
        set.update('added_changed', ADDED)
        self.failIf(delegate.hasUID('added_changed'))
        set.update('added_changed', CHANGED)
        self.failIf(delegate.hasUID('added_changed'))
        set.update('added_changed', CHANGED)
        self.failIf(delegate.hasUID('added_changed'))
        set.process()
        self.failUnless(delegate.hasUID('added_changed'))
        self.assertEqual(delegate.getUIDCount('added_changed'), 0)

    def test_process_remove(self):
        delegate = self._makeDelegate()
        set = self._makeOne(delegate=delegate)
        self.failIf(delegate.hasUID('removed'))
        set.update('removed', REMOVED)
        self.failIf(delegate.hasUID('removed'))
        set.process()
        self.failIf(delegate.hasUID('removed'))

    def test_process_add_and_remove(self):
        delegate = self._makeDelegate()
        set = self._makeOne(delegate=delegate)
        self.failIf(delegate.hasUID('added_removed'))
        set.update('added_removed', ADDED)
        self.failIf(delegate.hasUID('added_removed'))
        set.update('added_removed', REMOVED)
        self.failIf(delegate.hasUID('added_removed'))
        set.process()
        self.failIf(delegate.hasUID('added_removed'))


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(CatalogEventQueueSetTests),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/QueueCatalog/tests/test_CatalogEventQueue.py
# Compiled at: 2008-05-13 06:38:33
"""QueueCatalog tests.

$Id: test_CatalogEventQueue.py 86692 2008-05-13 10:38:28Z andreasjung $
"""
import os, shutil, tempfile, unittest, Testing, transaction, Zope2
Zope2.startup()
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.QueueCatalog.CatalogEventQueue import CatalogEventQueue
from Products.QueueCatalog.CatalogEventQueue import ADDED
from Products.QueueCatalog.CatalogEventQueue import CHANGED
from Products.QueueCatalog.CatalogEventQueue import CHANGED_ADDED
from Products.QueueCatalog.CatalogEventQueue import REMOVED
from Products.QueueCatalog.CatalogEventQueue import SAFE_POLICY
from Products.QueueCatalog.CatalogEventQueue import ALTERNATIVE_POLICY
from Products.QueueCatalog.QueueCatalog import QueueCatalog
from OFS.Application import Application
from OFS.Folder import Folder
from Testing.ZopeTestCase.base import TestCase
from ZODB.POSException import ConflictError

class QueueConflictTests(unittest.TestCase):
    __module__ = __name__

    def _setAlternativePolicy(self):
        self.queue._conflict_policy = ALTERNATIVE_POLICY
        self.queue._p_jar.transaction_manager.commit()
        self.queue2._p_jar.sync()
        self.assertEquals(self.queue._conflict_policy, ALTERNATIVE_POLICY)
        self.assertEquals(self.queue2._conflict_policy, ALTERNATIVE_POLICY)

    def _insane_update(self, queue, uid, etype):
        data = queue._data
        current = data.get(uid)
        if current is not None:
            (generation, current) = current
            if (current is ADDED or current is CHANGED_ADDED) and etype is CHANGED:
                etype = CHANGED_ADDED
        else:
            generation = 0
        data[uid] = (generation + 1, etype)
        queue._p_changed = 1
        return

    def openDB(self):
        from ZODB.FileStorage import FileStorage
        from ZODB.DB import DB
        self.dir = tempfile.mkdtemp()
        self.storage = FileStorage(os.path.join(self.dir, 'testQCConflicts.fs'))
        self.db = DB(self.storage)

    def setUp(self):
        self.openDB()
        queue = CatalogEventQueue()
        tm1 = transaction.TransactionManager()
        self.conn1 = self.db.open(transaction_manager=tm1)
        r1 = self.conn1.root()
        r1['queue'] = queue
        del queue
        self.queue = r1['queue']
        tm1.commit()
        tm2 = transaction.TransactionManager()
        self.conn2 = self.db.open(transaction_manager=tm2)
        r2 = self.conn2.root()
        self.queue2 = r2['queue']
        ignored = dir(self.queue2)

    def tearDown(self):
        transaction.abort()
        del self.queue
        del self.queue2
        if self.storage is not None:
            self.storage.close()
            self.storage.cleanup()
            shutil.rmtree(self.dir)
        return

    def test_rig(self):
        self.assertEqual(self.queue._p_serial, self.queue2._p_serial)

    def test_simpleConflict(self):
        for n in range(10):
            self.queue.update('/f%i' % n, ADDED)

        self.queue._p_jar.transaction_manager.commit()
        self.assertEqual(len(self.queue), 10)
        self.assertEqual(len(self.queue2), 0)
        for n in range(10):
            self.queue2.update('/g%i' % n, ADDED)

        self.assertEqual(len(self.queue), 10)
        self.assertEqual(len(self.queue2), 10)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue._p_jar.sync()
        self.queue2._p_jar.sync()
        self.assertEqual(len(self.queue), 20)
        self.assertEqual(len(self.queue2), 20)

    def test_unresolved_add_after_something(self):
        from Products.QueueCatalog.QueueCatalog import logger
        logger.disabled = 1
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self.queue2.update('/f0', ADDED)
        self.queue2.update('/f0', CHANGED)
        self.queue2._p_jar.transaction_manager.commit()
        self._insane_update(self.queue, '/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', ADDED)
        self.assertRaises(ConflictError, self.queue2._p_jar.transaction_manager.commit)
        logger.disabled = 0

    def test_resolved_add_after_nonremoval(self):
        self._setAlternativePolicy()
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self.queue2.update('/f0', ADDED)
        self.queue2.update('/f0', CHANGED)
        self.queue2._p_jar.transaction_manager.commit()
        self._insane_update(self.queue, '/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', ADDED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue._p_jar.sync()
        self.queue2._p_jar.sync()
        self.assertEquals(len(self.queue), 1)
        self.assertEquals(len(self.queue2), 1)
        event1 = self.queue.getEvent('/f0')
        event2 = self.queue2.getEvent('/f0')
        self.failUnless(event1 == event2 == CHANGED_ADDED)

    def test_resolved_add_after_removal(self):
        self._setAlternativePolicy()
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self.queue2.update('/f0', ADDED)
        self.queue2.update('/f0', CHANGED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue.update('/f0', REMOVED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', ADDED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue._p_jar.sync()
        self.queue2._p_jar.sync()
        self.assertEquals(len(self.queue), 1)
        self.assertEquals(len(self.queue2), 1)
        event1 = self.queue.getEvent('/f0')
        event2 = self.queue2.getEvent('/f0')
        self.failUnless(event1 == event2 == REMOVED)

    def test_unresolved_new_old_current_all_different(self):
        from Products.QueueCatalog.QueueCatalog import logger
        logger.disabled = 1
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', REMOVED)
        self.assertRaises(ConflictError, self.queue2._p_jar.transaction_manager.commit)
        logger.disabled = 0

    def test_resolved_new_old_current_all_different(self):
        self._setAlternativePolicy()
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', REMOVED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue._p_jar.sync()
        self.queue2._p_jar.sync()
        self.assertEquals(len(self.queue), 1)
        self.assertEquals(len(self.queue2), 1)
        event1 = self.queue.getEvent('/f0')
        event2 = self.queue2.getEvent('/f0')
        self.failUnless(event1 == event2 == CHANGED_ADDED)

    def test_unresolved_new_old_current_all_different_2(self):
        from Products.QueueCatalog.QueueCatalog import logger
        logger.disabled = 1
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self.queue2.update('/f0', ADDED)
        self.queue2.update('/f0', CHANGED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', REMOVED)
        self.assertRaises(ConflictError, self.queue2._p_jar.transaction_manager.commit)
        logger.disabled = 0

    def test_resolved_new_old_current_all_different_2(self):
        self._setAlternativePolicy()
        self.queue.update('/f0', ADDED)
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self.queue2.update('/f0', ADDED)
        self.queue2.update('/f0', CHANGED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue.update('/f0', CHANGED)
        self.queue._p_jar.transaction_manager.commit()
        self._insane_update(self.queue2, '/f0', REMOVED)
        self.queue2._p_jar.transaction_manager.commit()
        self.queue._p_jar.sync()
        self.queue2._p_jar.sync()
        self.assertEquals(len(self.queue), 1)
        self.assertEquals(len(self.queue2), 1)
        event1 = self.queue.getEvent('/f0')
        event2 = self.queue2.getEvent('/f0')
        self.failUnless(event1 == event2 == REMOVED)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(QueueConflictTests),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
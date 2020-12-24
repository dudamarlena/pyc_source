# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/QueueCatalog/tests/test_QueueCatalog.py
# Compiled at: 2008-05-13 06:38:33
__doc__ = 'QueueCatalog tests.\n\n$Id: test_QueueCatalog.py 86692 2008-05-13 10:38:28Z andreasjung $\n'
import logging, unittest, cStringIO, Testing, Zope2
Zope2.startup()
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.QueueCatalog.QueueCatalog import QueueCatalog
from OFS.Folder import Folder
from Testing.ZopeTestCase.base import TestCase

class QueueCatalogTests(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.app.real_cat = ZCatalog('real_cat')
        self.app.real_cat.addIndex('id', 'FieldIndex')
        self.app.real_cat.addIndex('title', 'FieldIndex')
        self.app.real_cat.addIndex('meta_type', 'FieldIndex')
        self.app.queue_cat = QueueCatalog(3)
        self.app.queue_cat.id = 'queue_cat'
        self.app.queue_cat.manage_edit(location='/real_cat', immediate_indexes=['id', 'title'])

    def testAddObject(self):
        app = self.app
        app.f1 = Folder()
        app.f1.id = 'f1'
        self.assertEqual(app.queue_cat.manage_size(), 0)
        self.assertEqual(len(app.real_cat), 0)
        app.queue_cat.catalog_object(app.f1)
        self.assertEqual(app.queue_cat.manage_size(), 1)
        self.assertEqual(len(app.real_cat), 1)

    def testDeferMostIndexes(self):
        app = self.app
        app.f1 = Folder()
        app.f1.id = 'f1'
        app.queue_cat.catalog_object(app.f1)
        res = app.queue_cat.searchResults(id='f1')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 0)
        app.queue_cat.process()
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 1)

    def testPinpointIndexes(self):
        app = self.app
        app.queue_cat.setImmediateMetadataUpdate(True)
        app.queue_cat.setProcessAllIndexes(False)
        app.f1 = Folder()
        app.f1.id = 'f1'
        app.f1.title = 'Joe'
        app.queue_cat.catalog_object(app.f1, idxs=['id'])
        res = app.queue_cat.searchResults(id='f1')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(title='Joe')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 0)
        app.queue_cat.process()
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 1)
        app.f1.meta_type = 'Duck'
        app.f1.title = 'Betty'
        app.queue_cat.catalog_object(app.f1, idxs=['title'])
        res = app.queue_cat.searchResults(title='Joe')
        self.assertEqual(len(res), 0)
        res = app.queue_cat.searchResults(title='Betty')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 1)
        app.queue_cat.process()
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Duck')
        self.assertEqual(len(res), 0)
        app.f1.title = 'Susan'
        app.queue_cat.catalog_object(app.f1, idxs=['meta_type'])
        res = app.queue_cat.searchResults(title='Betty')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Duck')
        self.assertEqual(len(res), 0)
        app.queue_cat.process()
        res = app.queue_cat.searchResults(meta_type='Duck')
        self.assertEqual(len(res), 1)

    def testIndexOnce(self):
        app = self.app
        app.queue_cat.setImmediateMetadataUpdate(True)
        app.queue_cat.setProcessAllIndexes(False)
        app.f1 = Folder()
        app.f1.id = 'f1'
        app.f1.title = 'Joe'
        app.queue_cat.catalog_object(app.f1)
        res = app.queue_cat.searchResults(title='Joe')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 0)
        app.f1.title = 'Missed me'
        app.queue_cat.process()
        res = app.queue_cat.searchResults(title='Joe')
        self.assertEqual(len(res), 1)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 1)

    def testMetadataOnce(self):
        app = self.app
        app.queue_cat.setImmediateMetadataUpdate(True)
        app.queue_cat.setProcessAllIndexes(False)
        app.real_cat.addColumn('title')
        app.f1 = Folder()
        app.f1.id = 'f1'
        app.f1.title = 'Joe'
        app.queue_cat.catalog_object(app.f1)
        res = app.queue_cat.searchResults(id='f1')[0]
        self.assertEqual(res.title, 'Joe')
        app.f1.title = 'Betty'
        app.queue_cat.process()
        res = app.queue_cat.searchResults(id='f1')[0]
        self.assertEqual(res.title, 'Joe')
        app.queue_cat.setImmediateMetadataUpdate(False)
        app.queue_cat.catalog_object(app.f1)
        res = app.queue_cat.searchResults(id='f1')[0]
        self.assertEqual(res.title, 'Joe')
        app.queue_cat.process()
        res = app.queue_cat.searchResults(id='f1')[0]
        self.assertEqual(res.title, 'Betty')

    def testLogCatalogErrors(self):
        from Products.QueueCatalog.QueueCatalog import logger
        logger.propagate = 0
        fake_file = cStringIO.StringIO()
        fake_log_handler = logging.StreamHandler(fake_file)
        logger.addHandler(fake_log_handler)
        app = self.app
        app.f1 = Folder()
        app.f1.id = 'f1'
        app.queue_cat.catalog_object(app.f1)
        app.real_cat.catalog_object = lambda : None
        app.queue_cat.process()
        del app.real_cat.catalog_object
        output = fake_file.getvalue()
        self.failUnless(output.startswith('error cataloging object'))
        fake_file.seek(0)
        app.queue_cat.setImmediateRemoval(False)
        app.queue_cat.uncatalog_object(app.queue_cat.uidForObject(app.f1))
        app.real_cat.uncatalog_object = lambda : None
        app.queue_cat.process()
        del app.real_cat.uncatalog_object
        output = fake_file.getvalue()
        self.failUnless(output.startswith('error uncataloging object'))
        fake_file.close()
        fake_log_handler.close()
        logger.removeHandler(fake_log_handler)
        logger.propagate = 1

    def testQueueProcessingLimit(self):
        app = self.app
        for n in range(100):
            f = Folder()
            f.id = 'f%d' % n
            setattr(app, f.id, f)
            f = getattr(app, f.id)
            app.queue_cat.catalog_object(f)

        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 0)
        app.queue_cat.process(max=10)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 10)
        app.queue_cat.process(max=25)
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 35)
        app.queue_cat.process()
        res = app.queue_cat.searchResults(meta_type='Folder')
        self.assertEqual(len(res), 100)

    def testGetIndexInfo(self):
        info = self.app.queue_cat.getIndexInfo()
        self.assertEqual(len(info), 3)
        self.assert_({'id': 'id', 'meta_type': 'FieldIndex'} in info)
        self.assert_({'id': 'meta_type', 'meta_type': 'FieldIndex'} in info)
        self.assert_({'id': 'title', 'meta_type': 'FieldIndex'} in info)

    def testRealCatSpecifiesUids(self):

        def stupidUidMaker(self, obj):
            return '/stupid/uid'

        ZCatalog.uidForObject = stupidUidMaker
        self.assertEqual(self.app.queue_cat.uidForObject(None), '/stupid/uid')
        return

    def testImmediateDeletion(self):
        app = self.app
        app.test_cat = QueueCatalog(1000)
        app.test_cat.id = 'test_cat'
        app.test_cat.manage_edit(location='/real_cat', immediate_indexes=['id'], immediate_removal=1)
        for n in range(20):
            f = Folder()
            f.id = 'f%d' % n
            setattr(app, f.id, f)
            f = getattr(app, f.id)
            app.test_cat.catalog_object(f)

        self.assertEqual(app.test_cat.manage_size(), 20)
        app.test_cat.uncatalog_object(getattr(app, 'f1').getPhysicalPath())
        self.assertEqual(app.test_cat.manage_size(), 19)
        del app.test_cat


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(QueueCatalogTests),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
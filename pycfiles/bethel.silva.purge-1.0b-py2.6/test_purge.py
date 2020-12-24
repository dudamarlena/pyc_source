# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/silva/purge/tests/test_purge.py
# Compiled at: 2012-05-25 11:11:07
from five import grok
from zope.component import getUtility, queryUtility, getAdapters
from zope.event import notify
from DateTime import DateTime
from zope.publisher.browser import TestRequest
from ZPublisher.pubevents import PubStart, PubSuccess
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from plone.registry.interfaces import IRegistry
from plone.cachepurging.hooks import KEY as URL_QUEUE_KEY
from plone.cachepurging.interfaces import IPurger
from plone.cachepurging.utils import getPathsToPurge
from z3c.caching.purge import Purge
from z3c.caching.interfaces import IPurgePaths
from PurgingTestCase import PurgingTestCase
from bethel.silva.purge.interfaces import IPurgingService
from bethel.silva.purge.service import registry_map
from bethel.silva.purge import testing

class BetterTestRequest(TestRequest):
    """Stupid TestRequest does not support annotations.  Seems everything has
       annotations these days, which makes writing tests impossible.  Add
       back in support for request.other, so annotations are possible
    """
    grok.implements(IAttributeAnnotatable)

    def __init__(self, *args, **kw):
        self.other = {}
        super(BetterTestRequest, self).__init__(*args, **kw)

    def __setitem__(self, key, value):
        self.other[key] = value

    def keys(self):
        k = set(super(BetterTestRequest, self).keys())
        k.add(self.other.keys())
        return list(k)

    def get(self, key, default=None):
        marker = object()
        result = super(BetterTestRequest, self).get(key, marker)
        if result is not marker:
            return result
        return self.other.get(key, default)


class PurgeTestCase(PurgingTestCase):

    def setUp(self):
        super(PurgeTestCase, self).setUp()
        self.browser = self.layer.get_browser()
        self.browser.options.handle_errors = False
        self.root = self.layer.get_application()
        self.doc = self.layer.addObject(self.root, 'Document', 'doc', product='SilvaDocument', title='doc')
        self.now = DateTime()
        self.layer.addObject(self.root, 'Folder', 'f', title='f')
        self.layer.addObject(self.root.f, 'Document', 'index', product='SilvaDocument', title='index')
        self.service = getUtility(IPurgingService, context=self.root)
        config = {('', 'root'): ['/blah/', '/blah2']}
        self.service.set_path_mappings(config)
        self.service.set_enabled(True)
        reg = getUtility(IRegistry, context=self.root)
        reg[registry_map['enabled']] = True
        reg[registry_map['cachingProxies']] = ('http://localhost:6081/', )

    def test_notify(self):
        version = self.doc.get_editable()
        notify(Purge(version))
        self.assertEquals(self.service.test_counter.pop(), version)
        self.service.test_counter = []
        self.doc.set_unapproved_version_publication_datetime(self.now)
        self.doc.approve_version()
        self.assertListEqual(self.service.test_counter, [version, version])

    def test_publishing_notify(self):
        version = self.doc.get_editable()
        request = BetterTestRequest()
        annotations = IAnnotations(request)
        self.assertFalse(annotations.has_key(URL_QUEUE_KEY))
        notify(PubStart(request))
        self.doc.set_unapproved_version_publication_datetime(self.now)
        self.doc.approve_version()
        annotations = IAnnotations(request)
        self.assertTrue(annotations.has_key(URL_QUEUE_KEY))
        queue = IAnnotations(request)[URL_QUEUE_KEY]
        self.assertTrue(len(queue) > 0)
        notify(PubSuccess(request))
        purger = queryUtility(IPurger)
        purger.stopThreads(wait=True)

    def test_publishing_notify_index(self):
        version = self.doc.get_editable()
        request = BetterTestRequest()
        annotations = IAnnotations(request)
        self.assertFalse(annotations.has_key(URL_QUEUE_KEY))
        notify(PubStart(request))
        self.root.f.index.set_unapproved_version_publication_datetime(self.now)
        self.root.f.index.approve_version()
        annotations = IAnnotations(request)
        self.assertTrue(annotations.has_key(URL_QUEUE_KEY))
        queue = IAnnotations(request)[URL_QUEUE_KEY]
        self.assertTrue('/blah2/f/index' in queue)
        self.assertTrue('/blah2/f/' in queue)
        self.assertTrue('/blah2/f' in queue)
        self.assertTrue('/blah/f/index' in queue)
        self.assertTrue('/blah/f/' in queue)
        self.assertTrue('/blah/f' in queue)
        notify(PubSuccess(request))
        purger = queryUtility(IPurger)
        purger.stopThreads(wait=True)

    def test_paths_to_purge(self):
        paths = set()
        item = self.doc.get_editable()
        for (name, pathProvider) in getAdapters((item,), IPurgePaths):
            paths.update(set(pathProvider.getRelativePaths()))
            paths.update(set(pathProvider.getAbsolutePaths()))

        self.assertTrue('/blah2/doc' in paths)
        self.assertTrue('/blah/doc' in paths)
        paths = set()
        for (name, pathProvider) in getAdapters((self.root.f,), IPurgePaths):
            paths.update(set(pathProvider.getRelativePaths()))
            paths.update(set(pathProvider.getAbsolutePaths()))

        self.assertTrue('/blah2/f' in paths)
        self.assertTrue('/blah2/f/' in paths)
        self.assertTrue('/blah/f' in paths)
        self.assertTrue('/blah/f/' in paths)

    def test_service_disabled(self):
        self.service.set_enabled(False)
        paths = set()
        item = self.doc.get_editable()
        for (name, pathProvider) in getAdapters((item,), IPurgePaths):
            paths.update(set(pathProvider.getRelativePaths()))
            paths.update(set(pathProvider.getAbsolutePaths()))

        self.assertListEqual(['/root/doc/0'], list(paths))

    def test_virtualhosting(self):
        reg = getUtility(IRegistry, context=self.root)
        reg[registry_map['virtualHosting']] = True
        reg[registry_map['domains']] = ('http://example.com:80', 'https://example.com:443')
        self.service.set_enabled(False)
        paths = set()
        item = self.doc.get_editable()
        for (name, pathProvider) in getAdapters((item,), IPurgePaths):
            paths.update(set(pathProvider.getRelativePaths()))
            paths.update(set(pathProvider.getAbsolutePaths()))

        self.assertListEqual(['/root/doc/0', '/doc'], paths)
        request = BetterTestRequest(environ={'VIRTUAL_URL_PARTS': ('a', 'b'), 'VirtualRootPhysicalPath': ('', 'root'), 
           'VIRTUAL_URL': 'http://example.com/doc'})
        paths = list(getPathsToPurge(item, request))
        self.assertTrue('/VirtualHostBase/http/example.com:80/root/VirtualHostRoot/doc' in paths)
        self.assertTrue('/VirtualHostBase/https/example.com:443/root/VirtualHostRoot/doc' in paths)

    def test_get_utility(self):
        ps = queryUtility(IPurgingService, context=self.root)
        self.assertFalse(ps is None)
        return


import unittest

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PurgeTestCase))
    return suite
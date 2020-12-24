# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.collection.proxy/inqbus/collection/proxy/tests/test_functionalities.py
# Compiled at: 2011-06-01 08:57:45
"""This is an integration "unit" test.
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from zope.component import getMultiAdapter, getAdapters
from Products.CMFCore.utils import getToolByName
from inqbus.collection.proxy.tests.base import InqbusCollectionProxyTestCase
import unittest

class TestSetup(InqbusCollectionProxyTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def afterSetUp(self):
        """
        """
        pass

    def beforeTearDown(self):
        """
        """
        pass

    def test_for_extended_fied(self):
        """ After the installation the collections shoult have a new field.
        Lets Check that!
        We create a new Topic and try to set the field.
        """
        self.setRoles('Manager')
        self.portal.invokeFactory('Topic', 'testcollection')
        self.failUnless(hasattr(self.portal.testcollection, 'boolean_proxy_field'))

    def test_different_links(self):
        """ The modified collectionview should show 2 differen links, weather the
        boolean_proxy_field is set or not. To try this, I create a object and determine
        the url which is build for it, according to the field.
        """
        self.setRoles('Manager')
        self.portal.invokeFactory('Topic', 'testcollection')
        self.portal.invokeFactory('Document', 'testsite')
        testcollection = self.portal.testcollection
        testsite = self.portal.portal_catalog(SearchableText='testsite')[0]
        from inqbus.collection.proxy.browser.collectionproxyview import CollectionProxyView
        proxyview = CollectionProxyView(testcollection, self.portal.REQUEST)
        self.assertEqual(proxyview.get_item_url(testsite), 'http://nohost/plone/testsite')
        testcollection.boolean_proxy_field = True
        self.assertEqual(proxyview.get_item_url(testsite), 'http://nohost/plone/testcollection/»/plone/testsite')
        testcollection.boolean_proxy_field = False
        testsite = self.portal.testsite
        self.assertEqual(proxyview.get_item_url(testsite), 'http://nohost/plone/testsite')

    def test_traversal_hasMoreNames(self):
        """ 
        """
        from inqbus.collection.proxy.traversal import CollectionProxyTraverser
        testrequest = self.portal.REQUEST
        testrequest['TraversalRequestNameStack'] = []
        traverser_without_stack = CollectionProxyTraverser(self.portal, testrequest)
        self.failUnless(not traverser_without_stack.hasMoreNames())
        testrequest['TraversalRequestNameStack'] = [
         'test0', 'test1', 'test2', 'test3']
        traverser_with_stack = CollectionProxyTraverser(self.portal, testrequest)
        self.failUnless(traverser_with_stack.hasMoreNames())

    def test_traversal_nextName(self):
        """ The nextName function of the traverser takes the next value out of the 
        TraversalRequestNameStack. Here we test that.
        """
        from inqbus.collection.proxy.traversal import CollectionProxyTraverser
        testrequest = self.portal.REQUEST
        testrequest['TraversalRequestNameStack'] = ['test0', 'test1', 'test2', 'test3']
        traverser = CollectionProxyTraverser(self.portal, testrequest)
        self.assertEqual(traverser.nextName(), 'test3')
        self.assertEqual(traverser.nextName(), 'test2')
        self.assertEqual(traverser.nextName(), 'test1')
        self.assertEqual(traverser.nextName(), 'test0')

    def test_traversal_get_source_object(self):
        """ the get_source_function from the traverser shoul get via restrictedTraverse the object
        and return it. If the object does not exists, it return none
        """
        from inqbus.collection.proxy.traversal import CollectionProxyTraverser
        traverser = CollectionProxyTraverser(self.portal, self.portal.REQUEST)
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Folder', 'testfolder')
        self.portal.testfolder.invokeFactory('Document', 'testsite')
        testobject = self.portal.testfolder.testsite
        self.assertEqual(traverser.get_source_object(relpath=testobject.absolute_url_path()).__repr__(), '<ATDocument at /plone/testfolder/testsite>')
        self.failUnless(not traverser.get_source_object(relpath='/plone/testfolder/testsite-2'))

    def test_traversal_publishTraverse(self):
        """
        """
        self.setRoles('Manager')
        from inqbus.collection.proxy.traversal import CollectionProxyTraverser
        self.portal.invokeFactory('Topic', 'testcollection_with_true')
        testcollection_with_true = self.portal.testcollection_with_true
        testcollection_with_true.boolean_proxy_field = True
        self.portal.invokeFactory('Folder', 'testfolder')
        self.portal.testfolder.invokeFactory('Document', 'testsite')
        testsite = self.portal.testfolder.testsite
        proxied_path = '/»/' + ('/').join(testsite.absolute_url_path().split('/')[2:])
        proxied_url = unicode(testcollection_with_true.absolute_url() + proxied_path)
        proxy_request = self.portal.REQUEST
        proxy_name_stack = proxied_path.split('/')
        proxy_request['URL'] = proxied_url
        proxy_name_stack.reverse()
        proxy_name_stack.pop()
        proxy_name = proxy_name_stack.pop(-1)
        proxy_request['TraversalRequestNameStack'] = proxy_name_stack
        traverser_with_true = CollectionProxyTraverser(testcollection_with_true, proxy_request)
        self.assertEqual(traverser_with_true.publishTraverse(proxy_request, proxy_name).__repr__(), '<ATDocument at /plone/testcollection_with_true/testsite>')
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/tests/test_add_content_types.py
# Compiled at: 2010-08-19 05:10:30
"""
test_add_content_types.py

Created by Manabu Terada on 2010-08-03.
Copyright (c) 2010 CMScom. All rights reserved.
"""
import random
from Products.CMFCore.utils import getToolByName
import c2.app.tweemanager, base

class TestContentTypes(base.BaseTestCase):
    """ TopPage test """

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('c2.app.shorturl')
        self.css = self.portal.portal_css
        self.skins = self.portal.portal_skins
        self.types = self.portal.portal_types
        self.factory = self.portal.portal_factory
        self.workflow = self.portal.portal_workflow
        self.properties = self.portal.portal_properties
        self.g_allow_types = [
         'ShortUrlFolder']
        self.no_g_allow_types = [
         'ShortUrl']
        self.folder_into_types = [
         (
          'ShortUrl', ('ShortUrlFolder', ))]
        self.addingtypes = self.g_allow_types + self.no_g_allow_types

    def test_types_installed(self):
        print self.types.objectIds()
        for t in self.addingtypes:
            self.failUnless(t in self.types.objectIds())

    def test_portal_factorySetup(self):
        print self.factory.getFactoryTypes()
        for t in self.addingtypes:
            self.failUnless(t in self.factory.getFactoryTypes())

    def test_permission(self):
        permissions = [ p['name'] for p in self.app.permission_settings() ]
        for t in self.addingtypes:
            p = 'c2.app.shorturl: Add %s' % t
            self.failUnless(p in permissions)

    def test_global_creating(self):
        self.setRoles(['Manager'])
        allow_content_types = [ al.id for al in self.portal.allowedContentTypes() ]
        for t in self.g_allow_types:
            self.failUnless(t in allow_content_types)
            id = t + '1'
            self.portal.invokeFactory(t, id)
            obj = getattr(self.portal, id)
            self.failUnless(self.portal.hasObject(id))
            print id

        for t in self.no_g_allow_types:
            self.failUnless(t not in allow_content_types)

    def test_folder_into_creating(self):
        self.setRoles(['Manager'])
        for (t, ps) in self.folder_into_types:
            parent = self.portal
            for p in ps:
                base_parent = parent
                pid = p + str(random.random())
                base_parent.invokeFactory(p, pid)
                parent = getattr(base_parent, pid)
                self.failUnless(base_parent.hasObject(pid))
                self.failUnless(parent())

            allw_content_types = [ al.id for al in parent.allowedContentTypes() ]
            self.failUnless(t in allw_content_types)
            tid = t + '1'
            parent.invokeFactory(t, tid)
            tobj = getattr(parent, tid)
            self.failUnless(parent.hasObject(tid))
            print tobj.absolute_url(), tobj.id
            self.failUnless(tobj())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestContentTypes))
    return suite
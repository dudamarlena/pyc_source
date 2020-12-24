# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/tests/test_directive.py
# Compiled at: 2010-11-18 05:53:01
import os, unittest, zope.component
from cStringIO import StringIO
from zope.configuration.xmlconfig import XMLConfig, xmlconfig
from zope.publisher.browser import TestRequest
from zope.testing import cleanup
import zope.browserresource, falkolab.cacheburster
from zope.browserresource.file import FileResource
from falkolab.cacheburster.interfaces import IVersionRule, IVersionedResourceLayer, IVersionManager
from falkolab.cacheburster.rule import CacheBursterRule
from falkolab.cacheburster.version import MD5VersionManager, CRC32VersionManager, FileVersionManager
from falkolab.cacheburster import version
from zope.interface.declarations import directlyProvides
from falkolab.cacheburster.testing import ITestSkin
tests_path = os.path.join(os.path.dirname(falkolab.cacheburster.__file__), 'tests')
template = "<configure\n   xmlns='http://namespaces.zope.org/zope'\n   xmlns:browser='http://namespaces.zope.org/browser'\n   i18n_domain='zope'>\n   %s\n   </configure>"
request = TestRequest()
directlyProvides(request, ITestSkin)

class Test(cleanup.CleanUp, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        XMLConfig('meta.zcml', zope.browserresource)()
        XMLConfig('meta.zcml', falkolab.cacheburster)()
        zope.component.provideAdapter(MD5VersionManager, name='md5')
        zope.component.provideAdapter(CRC32VersionManager, name='crc32')
        file = os.path.join(tests_path, 'testfiles', 'version.txt')
        zope.component.provideAdapter(FileVersionManager(file), (
         version.IResource, IVersionedResourceLayer), IVersionManager, name='versionfile')

    def tearDown(self):
        super(Test, self).tearDown()

    def testVersionAdapters(self):
        path = os.path.join(tests_path, 'testfiles', 'script.js')
        xmlconfig(StringIO(template % '\n            <browser:resource\n                name="script.js"\n                file="%s"\n                />\n             ' % path))
        resource = zope.component.getAdapter(request, name='script.js')
        self.assertTrue(isinstance(resource, FileResource))
        self.assertNotEqual(zope.component.queryMultiAdapter((resource, request), name='crc32'), None)
        self.assertNotEqual(zope.component.queryMultiAdapter((resource, request), name='md5'), None)
        return

    def testRules(self):
        path = os.path.join(tests_path, 'testfiles', 'script.js')
        xmlconfig(StringIO(template % '\n            <browser:resource\n                name="script.js"\n                file="%s"\n                />\n                \n            <browser:cacheburster \n                from="(.*)\\.js" \n                to="\\1.{version}.js"\n                fileset="testfiles/*.js"\n                />\n                \n            <browser:cacheburster \n                from="(.*)-module\\.js" \n                to="\\1-module.js?{version}"\n                manager="md5"\n                />           \n            ' % path))
        resource = zope.component.getAdapter(request, name='script.js')
        self.assertTrue(isinstance(resource, FileResource))
        n = 0
        for (name, rule) in zope.component.getAdapters((resource,), IVersionRule):
            n += 1
            self.assertTrue(isinstance(rule, CacheBursterRule))

        self.assertEqual(n, 2)


def test_suite():
    return unittest.makeSuite(Test)
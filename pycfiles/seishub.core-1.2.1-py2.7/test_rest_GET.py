# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest_GET.py
# Compiled at: 2010-12-23 17:42:41
"""
A test suite for B{GET} request on REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.processor import POST, PUT, DELETE, GET, Processor
from seishub.core.processor.resources.rest import RESTResource, RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
from sets import Set
from twisted.web import http
import unittest
XML_BASE_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>%s</blahblah1>\n    <blah2>%s</blah2>\n  </blah1>\n</testml>'
XML_DOC = XML_BASE_DOC % ('üöäß', '5')
XML_DOC2 = XML_BASE_DOC % ('üöäß', '%d')

class AResourceType(Component):
    """
    A non versioned test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'get-test'
    resourcetype_id = 'notvc'
    version_control = False


class AResourceType2(Component):
    """
    Another test package and resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'get-test2'
    resourcetype_id = 'notvc'
    version_control = False


class AResourceType3(Component):
    """
    Another test package and resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'get-test'
    resourcetype_id = 'notvc2'
    version_control = False


class AVersionControlledResourceType(Component):
    """
    A version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'get-test'
    resourcetype_id = 'vc'
    version_control = True


class RestGETTests(SeisHubEnvironmentTestCase):
    """
    A test suite for GET request on REST resources.
    """

    def setUp(self):
        self.env.enableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)
        self.env.tree = RESTFolder()

    def tearDown(self):
        self.env.registry.db_deleteResourceType('get-test', 'vc')
        self.env.registry.db_deleteResourceType('get-test', 'notvc')
        self.env.registry.db_deletePackage('get-test')

    def test_getRoot(self):
        proc = Processor(self.env)
        data = proc.run(GET, '')
        data2 = proc.run(GET, '/')
        self.assertTrue(Set(data) == Set(data2))
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('get-test' in data)
        self.assertTrue('seishub' in data)
        self.assertFalse('get-test2' in data)

    def test_getPackage(self):
        proc = Processor(self.env)
        data = proc.run(GET, '/get-test')
        data2 = proc.run(GET, '/get-test')
        self.assertTrue(Set(data) == Set(data2))
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('notvc' in data)
        self.assertTrue('vc' in data)

    def test_getNotExistingPackage(self):
        proc = Processor(self.env)
        path = ''
        for _ in xrange(0, 5):
            path = path + '/yyy'
            try:
                proc.run(DELETE, path)
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_FOUND)

            try:
                proc.run(DELETE, path + '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_FOUND)

    def test_getDisabledPackage(self):
        proc = Processor(self.env)
        try:
            proc.run(DELETE, '/get-test2')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        try:
            proc.run(DELETE, '/get-test2/')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_getResourceTypeFolder(self):
        """
        Get content of a resource type folder.
        """
        proc = Processor(self.env)
        proc.run(POST, '/get-test/notvc/test.xml', StringIO(XML_DOC))
        data = proc.run(GET, '/get-test/notvc')
        data2 = proc.run(GET, '/get-test/notvc/')
        self.assertTrue(Set(data) == Set(data2))
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('test.xml' in data)
        data = proc.run(DELETE, '/get-test/notvc/test.xml')

    def test_getVersionControlledResourceTypeFolder(self):
        """
        Get content of a version controlled resource type folder.
        """
        proc = Processor(self.env)
        proc.run(POST, '/get-test/vc/test.xml', StringIO(XML_DOC2 % 11))
        proc.run(PUT, '/get-test/vc/test.xml', StringIO(XML_DOC2 % 22))
        proc.run(PUT, '/get-test/vc/test.xml', StringIO(XML_DOC2 % 33))
        proc.run(POST, '/get-test/vc/test2.xml', StringIO(XML_DOC2 % 111))
        proc.run(PUT, '/get-test/vc/test2.xml', StringIO(XML_DOC2 % 222))
        data = proc.run(GET, '/get-test/vc')
        data2 = proc.run(GET, '/get-test/vc/')
        self.assertTrue(Set(data) == Set(data2))
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('test.xml' in data)
        self.assertTrue('test2.xml' in data)
        self.assertEquals(data['test.xml'].revision, 3)
        self.assertEquals(data['test2.xml'].revision, 2)
        data = proc.run(DELETE, '/get-test/vc/test.xml')
        data = proc.run(DELETE, '/get-test/vc/test2.xml')

    def test_getNotExistingResourceType(self):
        proc = Processor(self.env)
        path = '/get-test'
        for _ in xrange(0, 5):
            path = path + '/yyy'
            try:
                proc.run(DELETE, path)
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_FOUND)

            try:
                proc.run(DELETE, path + '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_FOUND)

    def test_getDisabledResourceType(self):
        proc = Processor(self.env)
        try:
            proc.run(DELETE, '/get-test/notvc2')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        try:
            proc.run(DELETE, '/get-test/notvc2/')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_getResource(self):
        proc = Processor(self.env)
        proc.run(POST, '/get-test/notvc/test.xml', StringIO(XML_DOC))
        res1 = proc.run(GET, '/get-test/notvc/test.xml')
        data1 = res1.render(proc)
        res2 = proc.run(GET, '/get-test/notvc/test.xml/')
        data2 = res2.render(proc)
        self.assertTrue(isinstance(res1, RESTResource))
        self.assertTrue(isinstance(res2, RESTResource))
        self.assertTrue(Set(data1) == Set(data2))
        self.assertTrue(isinstance(data1, basestring))
        self.assertEquals(data1, XML_DOC)
        proc.run(DELETE, '/get-test/notvc/test.xml')

    def test_getRevision(self):
        proc = Processor(self.env)
        proc.run(POST, '/get-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/get-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/get-test/vc/test.xml', StringIO(XML_DOC))
        res1 = proc.run(GET, '/get-test/vc/test.xml/1')
        data1 = res1.render_GET(proc)
        res2 = proc.run(GET, '/get-test/vc/test.xml/1/')
        data2 = res2.render_GET(proc)
        self.assertTrue(isinstance(res1, RESTResource))
        self.assertTrue(isinstance(res2, RESTResource))
        self.assertTrue(data1 == data2)
        self.assertEquals(data1, XML_DOC)
        res3 = proc.run(GET, '/get-test/vc/test.xml/2')
        data3 = res3.render_GET(proc)
        self.assertEquals(data3, XML_DOC)
        res4 = proc.run(GET, '/get-test/vc/test.xml/2/')
        data4 = res4.render_GET(proc)
        self.assertEquals(data4, XML_DOC)
        proc.run(DELETE, '/get-test/vc/test.xml')

    def test_getRevisionFromNotVersionControlledResource(self):
        proc = Processor(self.env)
        proc.run(POST, '/get-test/notvc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/get-test/notvc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/get-test/notvc/test.xml', StringIO(XML_DOC))
        res1 = proc.run(GET, '/get-test/notvc/test.xml/1')
        data1 = res1.render(proc)
        res2 = proc.run(GET, '/get-test/notvc/test.xml/1/')
        data2 = res2.render(proc)
        self.assertTrue(isinstance(res1, RESTResource))
        self.assertTrue(isinstance(res2, RESTResource))
        self.assertTrue(Set(data1) == Set(data2))
        self.assertTrue(isinstance(data1, basestring))
        self.assertEquals(data1, XML_DOC)
        try:
            proc.run(GET, '/get-test/notvc/test.xml/2')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        try:
            proc.run(GET, '/get-test/notvc/test.xml/2/')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        proc.run(DELETE, '/get-test/notvc/test.xml')

    def test_dontHijackResources(self):
        """
        Don't hijack resources from different packages - see #65.
        """
        self.env.disableComponent(AResourceType2)
        self.env.disableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)
        proc = Processor(self.env)
        proc.run(POST, '/get-test/notvc/1', StringIO(XML_DOC))
        self.env.disableComponent(AResourceType)
        self.env.enableComponent(AResourceType2)
        try:
            proc.run(GET, '/get-test/notvc/1')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        try:
            proc.run(GET, '/get-test2/notvc/muh')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        try:
            proc.run(GET, '/get-test2/notvc/1')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        self.env.enableComponent(AResourceType)
        proc.run(POST, '/get-test/notvc/2', StringIO(XML_DOC))
        res = proc.run(GET, '/get-test/notvc/1')
        data = res.render_GET(proc)
        self.assertEquals(data, XML_DOC)
        proc.run(DELETE, '/get-test/notvc/1')
        proc.run(DELETE, '/get-test/notvc/2')
        self.env.registry.db_deleteResourceType('get-test2', 'notvc')
        self.env.registry.db_deletePackage('get-test2')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestGETTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
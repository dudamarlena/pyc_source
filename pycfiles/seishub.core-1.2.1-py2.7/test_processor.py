# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_processor.py
# Compiled at: 2010-12-23 17:42:41
"""
A test suite for the Processor.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.processor import MAXIMAL_URL_LENGTH, ALLOWED_HTTP_METHODS, POST, PUT, DELETE, GET, Processor
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import unittest
NOT_IMPLEMENTED_HTTP_METHODS = [
 'TRACE', 'OPTIONS', 'COPY', 'HEAD', 'PROPFIND',
 'PROPPATCH', 'MKCOL', 'CONNECT', 'PATCH',
 'LOCK', 'UNLOCK']
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n</testml>'
XML_DOC2 = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n  <hallowelt />\n</testml>'
XML_VC_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>%d</testml>'

class AResourceType(Component):
    """
    A non versioned test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'processor-test'
    resourcetype_id = 'notvc'
    version_control = False


class AVersionControlledResourceType(Component):
    """
    A version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'processor-test'
    resourcetype_id = 'vc'
    version_control = True


class ProcessorTests(SeisHubEnvironmentTestCase):
    """
    A test suite for the Processor.
    """

    def setUp(self):
        self.env.enableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)

    def tearDown(self):
        self.env.registry.db_deleteResourceType('processor-test', 'vc')
        self.env.registry.db_deleteResourceType('processor-test', 'notvc')
        self.env.registry.db_deletePackage('processor-test')

    def test_oversizedURL(self):
        """
        Request URL is restricted by MAXIMAL_URL_LENGTH.
        """
        proc = Processor(self.env)
        for method in ALLOWED_HTTP_METHODS:
            try:
                proc.run(method, 'a' * MAXIMAL_URL_LENGTH, '')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.REQUEST_URI_TOO_LONG)

    def test_processResourceType(self):
        proc = Processor(self.env)
        proc.path = '/xml/processor-test/notvc'
        data = proc.run(GET, '/xml/processor-test/notvc')
        self.assertTrue(isinstance(data, dict))
        data = proc.run(POST, '/xml/processor-test/notvc', StringIO(XML_DOC))
        self.assertFalse(data)
        self.assertEqual(proc.code, http.CREATED)
        self.assertTrue(isinstance(proc.headers, dict))
        self.assertTrue('Location' in proc.headers)
        location = proc.headers.get('Location')
        self.assertTrue(location.startswith(self.env.getRestUrl() + proc.path))
        location = location[len(self.env.getRestUrl()):]
        data = proc.run(GET, location)
        self.assertTrue(data, XML_DOC)
        data = proc.run(DELETE, location)
        self.assertFalse(data)
        self.assertEqual(proc.code, http.NO_CONTENT)

    def test_processResource(self):
        proc = Processor(self.env)
        data = proc.run(POST, '/xml/processor-test/notvc', StringIO(XML_DOC))
        self.assertFalse(data)
        self.assertEqual(proc.code, http.CREATED)
        self.assertTrue(isinstance(proc.headers, dict))
        self.assertTrue('Location' in proc.headers)
        location = proc.headers.get('Location')
        self.assertTrue(location.startswith(self.env.getRestUrl() + proc.path))
        location = location[len(self.env.getRestUrl()):]
        data = proc.run(GET, location).render_GET(proc)
        self.assertEquals(data, XML_DOC)
        proc.run(PUT, location, StringIO(XML_DOC2))
        data = proc.run(GET, location).render_GET(proc)
        self.assertNotEquals(data, XML_DOC)
        self.assertEquals(data, XML_DOC2)
        proc.run(DELETE, location)
        try:
            proc.run(GET, location).render_GET(proc)
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_processVCResource(self):
        """
        Test for a version controlled resource.
        """
        proc = Processor(self.env)
        data = proc.run(POST, '/xml/processor-test/vc', StringIO(XML_DOC))
        self.assertFalse(data)
        self.assertEqual(proc.code, http.CREATED)
        self.assertTrue(isinstance(proc.headers, dict))
        self.assertTrue('Location' in proc.headers)
        location = proc.headers.get('Location')
        self.assertTrue(location.startswith(self.env.getRestUrl() + proc.path))
        location = location[len(self.env.getRestUrl()):]
        data = proc.run(PUT, location, StringIO(XML_DOC2))
        self.assertFalse(data)
        self.assertEqual(proc.code, http.NO_CONTENT)
        self.assertTrue(isinstance(proc.headers, dict))
        self.assertTrue('Location' in proc.headers)
        location = proc.headers.get('Location')
        self.assertTrue(location.startswith(self.env.getRestUrl() + proc.path))
        location = location[len(self.env.getRestUrl()):]
        data = proc.run(GET, location).render_GET(proc)
        self.assertEquals(data, XML_DOC2)
        data = proc.run(GET, location + '/1').render_GET(proc)
        self.assertEquals(data, XML_DOC)
        data = proc.run(GET, location + '/2').render_GET(proc)
        self.assertEquals(data, XML_DOC2)
        try:
            data = proc.run(GET, location + '/3').render_GET(proc)
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        proc.run(DELETE, location)
        try:
            proc.run(GET, location).render_GET(proc)
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_strangeRequestPatterns(self):
        """
        Test strange request patterns.
        """
        proc = Processor(self.env)
        data = proc.run(GET, '///')
        self.assertTrue('xml' in data)
        data = proc.run(GET, '//./')
        self.assertTrue('xml' in data)
        data = proc.run(GET, '/xml//')
        self.assertTrue('seishub' in data)
        data = proc.run(GET, '//xml/')
        self.assertTrue('seishub' in data)
        data = proc.run(GET, '//////////////////////xml//////////////')
        self.assertTrue('seishub' in data)
        data = proc.run(GET, '/////////./////////////xml///////.////.///')
        self.assertTrue('seishub' in data)
        data = proc.run(GET, '//////////////////////xml/////////////seishub/')
        self.assertTrue('schema' in data)
        data = proc.run(GET, '/////////////////xml///////.//////seishub////')
        self.assertTrue('schema' in data)
        data = proc.run(GET, '/////////////////xml/../xml////seishub////')
        self.assertTrue('schema' in data)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProcessorTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
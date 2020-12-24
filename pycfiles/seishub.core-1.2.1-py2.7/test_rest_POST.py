# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest_POST.py
# Compiled at: 2011-01-03 17:15:11
"""
A test suite for POST requests on REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.processor import POST, PUT, DELETE, GET, Processor
from seishub.core.processor.resources import RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import glob, os, unittest
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n</testml>'
XML_VCDOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>%d</testml>'

class AResourceType(Component):
    """
    A non versioned test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'put-test'
    resourcetype_id = 'notvc'
    version_control = False


class AVersionControlledResourceType(Component):
    """
    A version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'put-test'
    resourcetype_id = 'vc'
    version_control = True


class RestPOSTTests(SeisHubEnvironmentTestCase):
    """
    A test suite for POST requests on REST resources.
    """

    def setUp(self):
        self.env.enableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)
        self.env.tree = RESTFolder()

    def tearDown(self):
        self.env.registry.db_deleteResourceType('put-test', 'notvc')
        self.env.registry.db_deleteResourceType('put-test', 'vc')
        self.env.registry.db_deletePackage('put-test')

    def test_putOnDeletedVersionControlledResource(self):
        """
        POST on deleted versionized resource should create new resource.
        """
        proc = Processor(self.env)
        proc.run(POST, '/put-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/put-test/vc/test.xml', StringIO(XML_VCDOC % 2))
        proc.run(PUT, '/put-test/vc/test.xml', StringIO(XML_VCDOC % 3))
        proc.run(DELETE, '/put-test/vc/test.xml')
        proc.run(POST, '/put-test/vc/test.xml', StringIO(XML_VCDOC % 10))
        data = proc.run(GET, '/put-test/vc/test.xml/1').render_GET(proc)
        self.assertEqual(data, XML_VCDOC % 10)
        proc.run(DELETE, '/put-test/vc/test.xml')

    def test_putHeadersWithGivenFilename(self):
        """
        Successful POST request returns Location header and 201 status code.
        """
        proc = Processor(self.env)
        proc.run(POST, '/put-test/notvc/test.xml', StringIO(XML_DOC))
        self.assertTrue('Location' in proc.headers)
        self.assertEquals(proc.headers.get('Location'), self.env.getRestUrl() + '/put-test/notvc/test.xml')
        self.assertEquals(proc.code, http.CREATED)
        proc.run(DELETE, '/put-test/notvc/test.xml')

    def test_putHeadersWithoutGivenFilename(self):
        """
        Successful POST request returns Location header and 201 status code.
        """
        proc = Processor(self.env)
        proc.run(POST, '/put-test/notvc', StringIO(XML_DOC))
        self.assertTrue('Location' in proc.headers)
        loc = proc.headers.get('Location')
        url = self.env.getRestUrl() + '/put-test/notvc/'
        self.assertTrue(loc.startswith(url))
        self.assertTrue(int(loc.split('/')[(-1)]))
        self.assertEquals(proc.code, http.CREATED)
        proc.run(DELETE, loc[len(self.env.getRestUrl()):])

    def test_putOnExistingResource(self):
        """
        Put request on an already existing resource.
        """
        proc = Processor(self.env)
        proc.run(POST, '/put-test/notvc/test.xml', StringIO(XML_DOC))
        try:
            proc.run(POST, '/put-test/notvc/test.xml', StringIO(XML_DOC))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/put-test/notvc/test.xml')

    def test_putOnExistingVersionControlledResource(self):
        """
        Put request on an already existing version controlled resource.
        """
        proc = Processor(self.env)
        proc.run(POST, '/put-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/put-test/vc/test.xml', StringIO(XML_DOC))
        try:
            proc.run(POST, '/put-test/vc/test.xml', StringIO(XML_DOC))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/put-test/vc/test.xml')

    def test_invalidResourceIDs(self):
        """
        Resource names have to be alphanumeric, start with a character
        """
        proc = Processor(self.env)
        try:
            proc.run(POST, '/put-test/notvc/üö$%&', StringIO(XML_DOC))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

    def test_putUTF8EncodedDocuments(self):
        """
        Tests from a UTF-8 conformance test suite by M. Kuhn and M. Duerst.
        
        @see: L{http://www.w3.org/2001/06/utf-8-test/}.
        """
        proc = Processor(self.env)
        path = os.path.dirname(__file__)
        files = glob.glob(os.path.join(path, 'data', 'utf-8-tests', '*.xml'))
        for file in files:
            data = open(file, 'rb').read().strip()
            proc.run(POST, '/put-test/notvc/test.xml', StringIO(data))
            result = proc.run(GET, '/put-test/notvc/test.xml').render_GET(proc)
            self.assertEqual(result, data)
            proc.run(DELETE, '/put-test/notvc/test.xml')

    def test_putJapaneseXMLDocuments(self):
        """
        Part of the W3C XML conformance test suite.
        
        This covers tests with different encoding and byte orders, e.g. UTF-16 
        with big and little endian. 
        
        @see: L{http://www.w3.org/XML/Test/}.
        """
        proc = Processor(self.env)
        path = os.path.dirname(__file__)
        files = glob.glob(os.path.join(path, 'data', 'japanese', '*.xml'))
        for file in files:
            data = open(file, 'rb').read()
            proc.run(POST, '/put-test/notvc/test.xml', StringIO(data))
            proc.run(DELETE, '/put-test/notvc/test.xml')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestPOSTTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
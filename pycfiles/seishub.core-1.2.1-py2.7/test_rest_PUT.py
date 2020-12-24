# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest_PUT.py
# Compiled at: 2011-01-03 17:15:11
"""
A test suite for PUT request on REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.processor import POST, PUT, DELETE, Processor
from seishub.core.processor.resources import RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
import glob, os, unittest
XML_DOC = '<?xml version="1.0" encoding="UTF-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n</testml>'

class AResourceType(Component):
    """
    A non versioned test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'post-test'
    resourcetype_id = 'notvc'
    version_control = False


class AVersionControlledResourceType(Component):
    """
    A version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'post-test'
    resourcetype_id = 'vc'
    version_control = True


class RestPUTTests(SeisHubEnvironmentTestCase):
    """
    A test suite for PUT request on REST resources.
    """

    def setUp(self):
        self.env.enableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)
        self.env.tree = RESTFolder()

    def tearDown(self):
        self.env.registry.db_deleteResourceType('post-test', 'notvc')
        self.env.registry.db_deleteResourceType('post-test', 'vc')
        self.env.registry.db_deletePackage('post-test')

    def test_postJapaneseXMLDocuments(self):
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
            proc.run(POST, '/post-test/notvc/test.xml', StringIO(data))
            proc.run(PUT, '/post-test/notvc/test.xml', StringIO(data))
            proc.run(DELETE, '/post-test/notvc/test.xml')

        for file in files:
            data = open(file, 'rb').read()
            proc.run(PUT, '/post-test/notvc/test.xml', StringIO(data))
            proc.run(PUT, '/post-test/notvc/test.xml', StringIO(data))
            proc.run(DELETE, '/post-test/notvc/test.xml')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestPUTTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
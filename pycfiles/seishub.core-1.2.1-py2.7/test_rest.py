# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest.py
# Compiled at: 2010-12-23 17:42:41
"""
A general test suite for REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.processor import POST, PUT, DELETE, MOVE, Processor
from seishub.core.processor.resources import RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import unittest
NOT_IMPLEMENTED_HTTP_METHODS = [
 'TRACE', 'COPY', 'PROPFIND', 'PROPPATCH',
 'MKCOL', 'CONNECT', 'PATCH', 'LOCK', 'UNLOCK']
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n</testml>'
XML_VC_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>%d</testml>'

class AResourceType(Component):
    """
    A non versioned test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'rest-test'
    resourcetype_id = 'notvc'
    version_control = False


class AVersionControlledResourceType(Component):
    """
    A version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'rest-test'
    resourcetype_id = 'vc'
    version_control = True


class RestTests(SeisHubEnvironmentTestCase):
    """
    A general test suite for REST resources.
    """

    def setUp(self):
        self.env.enableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)
        self.env.tree = RESTFolder()

    def tearDown(self):
        self.env.registry.db_deleteResourceType('rest-test', 'notvc')
        self.env.registry.db_deleteResourceType('rest-test', 'vc')
        self.env.registry.db_deletePackage('rest-test')

    def test_notImplementedMethodsOnRoot(self):
        proc = Processor(self.env)
        for method in NOT_IMPLEMENTED_HTTP_METHODS:
            try:
                proc.run(method, '')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_notImplementedMethodsOnPackage(self):
        proc = Processor(self.env)
        for method in NOT_IMPLEMENTED_HTTP_METHODS:
            try:
                proc.run(method, '/rest-test')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_notImplementedMethodsOnResourceType(self):
        proc = Processor(self.env)
        for method in NOT_IMPLEMENTED_HTTP_METHODS:
            try:
                proc.run(method, '/rest-test/notvc')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/notvc/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_notImplementedMethodsOnResource(self):
        proc = Processor(self.env)
        proc.run(POST, '/rest-test/notvc/test.xml', StringIO(XML_DOC))
        for method in NOT_IMPLEMENTED_HTTP_METHODS:
            try:
                proc.run(method, '/rest-test/notvc')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/notvc/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

        proc.run(DELETE, '/rest-test/notvc/test.xml')

    def test_notImplementedMethodsOnRevision(self):
        proc = Processor(self.env)
        proc.run(POST, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        for method in NOT_IMPLEMENTED_HTTP_METHODS:
            try:
                proc.run(method, '/rest-test/vc/2')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/vc/2/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

        proc.run(DELETE, '/rest-test/vc/test.xml')

    def test_forbiddenMethodsOnRoot(self):
        proc = Processor(self.env)
        for method in [PUT, POST, DELETE, MOVE]:
            try:
                proc.run(method, '')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_forbiddenMethodsOnPackage(self):
        proc = Processor(self.env)
        for method in [PUT, POST, DELETE, MOVE]:
            try:
                proc.run(method, '/rest-test')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_forbiddenMethodsOnResourceType(self):
        proc = Processor(self.env)
        for method in [PUT, DELETE, MOVE]:
            try:
                proc.run(method, '/rest-test/notvc')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/notvc/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_forbiddenMethodsOnRevision(self):
        proc = Processor(self.env)
        proc.run(POST, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        for method in [DELETE, MOVE, PUT, POST]:
            try:
                proc.run(method, '/rest-test/vc/test.xml/2')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/rest-test/vc/test.xml/2/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

        proc.run(DELETE, '/rest-test/vc/test.xml')

    def test_orderOfAddingResourcesMatters(self):
        """
        This test in this specific order failed in a previous revision.
        """
        proc = Processor(self.env)
        proc.run(POST, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/rest-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(POST, '/rest-test/notvc/test.xml', StringIO(XML_DOC))
        proc.run(DELETE, '/rest-test/vc/test.xml')
        proc.run(DELETE, '/rest-test/notvc/test.xml')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
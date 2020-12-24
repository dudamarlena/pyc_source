# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest_MOVE.py
# Compiled at: 2010-12-23 17:42:43
"""
A test suite for MOVE request on REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.processor import MAXIMAL_URL_LENGTH, POST, PUT, DELETE, GET, MOVE, Processor
from seishub.core.processor.resources import RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import unittest
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n</testml>'

class AResourceType(Component):
    """
    A non version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'move-test'
    resourcetype_id = 'notvc'
    version_control = False


class AVersionControlledResourceType(Component):
    """
    A version controlled test resource type.
    """
    implements(IResourceType, IPackage)
    package_id = 'move-test'
    resourcetype_id = 'vc'
    version_control = True


class RestMOVETests(SeisHubEnvironmentTestCase):
    """
    A test suite for MOVE request on REST resources.
    """

    def setUp(self):
        self.env.enableComponent(AVersionControlledResourceType)
        self.env.enableComponent(AResourceType)
        self.env.tree = RESTFolder()

    def tearDown(self):
        self.env.registry.db_deleteResourceType('move-test', 'notvc')
        self.env.registry.db_deleteResourceType('move-test', 'vc')
        self.env.registry.db_deletePackage('move-test')

    def test_moveWithoutDestinationHeader(self):
        """
        WebDAV HTTP MOVE request must submit a Destination header.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveWithoutAbsoluteDestination(self):
        """
        Destination header must be the absolute path to new destination.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': '/test/notvc/muh.xml'})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveWithOversizedDestination(self):
        """
        Destination path is restricted to MAX_URI_LENGTH chars.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/notvc/' + 'a' * (MAXIMAL_URL_LENGTH + 1)
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.REQUEST_URI_TOO_LONG)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveToOtherResourceType(self):
        """
        SeisHub allows moving resources only to the same resource type.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/vc/test2.xml'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveToInvalidResourceTypePath(self):
        """
        Expecting a xml directory before package and resource type.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/muh/notvc/test2.xml'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveToNonExistingResourceType(self):
        """
        SeisHub allows moving resources only to existing resource types.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/muh/kuh/test2.xml'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveWithoutFilename(self):
        """
        SeisHub expects as destination a full filename.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/vc/'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        uri = self.env.getRestUrl() + '/move-test/vc'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveToNewResource(self):
        """
        Resource was moved successfully to the specified destination URI.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/notvc/new.xml'
        data = proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
        self.assertFalse(data)
        self.assertEqual(proc.code, http.CREATED)
        self.assertTrue(isinstance(proc.headers, dict))
        self.assertTrue('Location' in proc.headers)
        location = proc.headers.get('Location')
        self.assertEquals(location, uri)
        try:
            proc.run(GET, '/move-test/notvc/test.xml').render_GET(proc)
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        data = proc.run(GET, '/move-test/notvc/new.xml').render_GET(proc)
        self.assertEqual(data, XML_DOC)
        uri = self.env.getRestUrl() + '/move-test/notvc/test.xml'
        proc.run(MOVE, '/move-test/notvc/new.xml', received_headers={'Destination': uri})
        proc.run(GET, '/move-test/notvc/test.xml').render_GET(proc)
        try:
            proc.run(GET, '/move-test/notvc/new.xml').render_GET(proc)
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveRevisionToRevision(self):
        """
        SeisHub does not allow to move revisions to revisions.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/vc/test.xml/1'
        try:
            proc.run(MOVE, '/move-test/vc/test.xml/2', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)

        proc.run(DELETE, '/move-test/vc/test.xml')

    def test_moveRevisionToNewResource(self):
        """
        SeisHub does not allow to move revisions to resources.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/vc/test.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/vc/muh.xml'
        try:
            proc.run(MOVE, '/move-test/vc/test.xml/1', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)

        proc.run(DELETE, '/move-test/vc/test.xml')

    def test_moveToExistingRevision(self):
        """
        SeisHub does not allow to move resources to revisions.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/vc/test1.xml', StringIO(XML_DOC))
        proc.run(POST, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/vc/test2.xml/1'
        try:
            proc.run(MOVE, '/move-test/vc/test1.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/vc/test1.xml')
        proc.run(DELETE, '/move-test/vc/test2.xml')

    def test_moveToNewRevision(self):
        """
        SeisHub does not allow to move a resource to a new revision.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/vc/test1.xml', StringIO(XML_DOC))
        proc.run(POST, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        proc.run(PUT, '/move-test/vc/test2.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/vc/test2.xml/4'
        try:
            proc.run(MOVE, '/move-test/vc/test1.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/vc/test1.xml')
        proc.run(DELETE, '/move-test/vc/test2.xml')

    def test_moveToExistingResource(self):
        """
        SeisHub does not allow to overwrite existing resources.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test1.xml', StringIO(XML_DOC))
        proc.run(POST, '/move-test/notvc/test2.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/notvc/test2.xml'
        try:
            proc.run(MOVE, '/move-test/notvc/test1.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/notvc/test1.xml')
        proc.run(DELETE, '/move-test/notvc/test2.xml')

    def test_moveBuiltinResource(self):
        """
        SeisHub builtin resources can't be renamed or moved.
        """
        proc = Processor(self.env)
        data = proc.run(GET, '/seishub/stylesheet')
        uri = '/seishub/stylesheet/' + data.keys()[0]
        to_uri = self.env.getRestUrl() + '/seishub/stylesheet/test.xml'
        try:
            proc.run(MOVE, uri, received_headers={'Destination': to_uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

    def test_moveToSameURI(self):
        """
        The source URI and the destination URI must not be the same.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/notvc/test.xml'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.FORBIDDEN)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveToInvalidResourcename(self):
        """
        Destination file name may not start with '@', '.', '_' or '-'.
        
        SeisHub restricts the destination filename to distinct between 
        mappers, @aliases and .properties.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/notvc/~test'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        uri = self.env.getRestUrl() + '/move-test/notvc/.test'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        uri = self.env.getRestUrl() + '/move-test/notvc/@test'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        uri = self.env.getRestUrl() + '/move-test/notvc/_test'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        uri = self.env.getRestUrl() + '/move-test/notvc/-test'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        uri = self.env.getRestUrl() + '/move-test/notvc/Aaz09_-.xml'
        proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
        uri = self.env.getRestUrl() + '/move-test/notvc/test.xml'
        proc.run(MOVE, '/move-test/notvc/Aaz09_-.xml', received_headers={'Destination': uri})
        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveLockedResource(self):
        """XXX: see ticket #38 - not implemented yet
        Locked resources can't be moved.
        """
        pass

    def test_moveToDifferentServer(self):
        """
        The destination URI is located on a different server.
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = 'http://somewhere:8080/move-test/notvc/test.xml'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_GATEWAY)

        proc.run(DELETE, '/move-test/notvc/test.xml')

    def test_moveToInvalidResourceID(self):
        """
        Resource names have to be alphanumeric, start with a character
        """
        proc = Processor(self.env)
        proc.run(POST, '/move-test/notvc/test.xml', StringIO(XML_DOC))
        uri = self.env.getRestUrl() + '/move-test/notvc/$%&'
        try:
            proc.run(MOVE, '/move-test/notvc/test.xml', received_headers={'Destination': uri})
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.BAD_REQUEST)

        proc.run(DELETE, '/move-test/notvc/test.xml')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestMOVETests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
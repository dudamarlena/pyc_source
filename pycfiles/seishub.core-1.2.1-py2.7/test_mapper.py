# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_mapper.py
# Compiled at: 2010-12-23 17:42:43
"""
A test suite for mapper resources.
"""
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IPackage
from seishub.core.processor import GET, PUT, DELETE, POST, HEAD, Processor
from seishub.core.packages.interfaces import IMapper
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import unittest
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<testml>\n  <blah1 id="3">\n    <blahblah1>üöäß</blahblah1>\n  </blah1>\n</testml>'

class APackage(Component):
    """
    A test package.
    """
    implements(IPackage)
    package_id = 'mapper-test'


class TestMapper(Component):
    """
    A test mapper.
    """
    implements(IMapper)
    mapping_url = '/mapper-test/testmapping'

    def process_GET(self, request):
        return 'muh'

    def process_PUT(self, request):
        pass

    def process_DELETE(self, request):
        pass

    def process_POST(self, request):
        pass


class TestMapper2(Component):
    """
    Another test mapper.
    """
    implements(IMapper)
    mapping_url = '/mapper-test/testmapping2'

    def process_GET(self, request):
        pass


class TestMapper3(Component):
    """
    And one more test mapper.
    """
    implements(IMapper)
    mapping_url = '/mapper-test/testmapping3'

    def process_GET(self, request):
        pass


class TestMapper4(Component):
    """
    And one more test mapper.
    """
    implements(IMapper)
    mapping_url = '/testmapping4'

    def process_GET(self, request):
        return 'MÜH'


class TestMapper5(Component):
    """
    An unregistered mapper.
    """
    implements(IMapper)
    mapping_url = '/mapper-test/testmapping5'

    def process_GET(self, request):
        pass


class MapperTests(SeisHubEnvironmentTestCase):
    """
    A test suite for mapper resources.
    """

    def setUp(self):
        self.env.enableComponent(APackage)
        self.env.enableComponent(TestMapper)
        self.env.enableComponent(TestMapper2)
        self.env.enableComponent(TestMapper3)
        self.env.enableComponent(TestMapper4)
        self.env.tree.update()

    def tearDown(self):
        self.env.registry.db_deletePackage('mapper-test')

    def test_checkRegisteredMappers(self):
        """
        Fetch mapper resource at different levels.
        """
        proc = Processor(self.env)
        data = proc.run(GET, '/')
        self.assertTrue('mapper-test' in data.keys())
        self.assertTrue('testmapping4' in data.keys())
        proc = Processor(self.env)
        data = proc.run(GET, '/mapper-test')
        self.assertTrue('testmapping' in data.keys())
        self.assertTrue('testmapping2' in data.keys())
        self.assertTrue('testmapping3' in data.keys())
        self.assertFalse('testmapping5' in data.keys())
        proc = Processor(self.env)
        data = proc.run(GET, '/mapper-test/testmapping')
        self.assertEqual(data, 'muh')
        data = proc.run(HEAD, '/testmapping4')
        self.assertEquals(data, 'MÜH')

    def test_dontReturnUnicodeFromMapper(self):
        """
        Unicodes returned from a mapper should be encoded into UTF-8 strings.
        """
        proc = Processor(self.env)
        data = proc.run(GET, '/testmapping4')
        self.assertFalse(isinstance(data, unicode))
        self.assertTrue(isinstance(data, basestring))
        self.assertEqual('MÜH', data)

    def test_notAllowedMethods(self):
        """
        Not allowed methods should raise an error.
        """
        proc = Processor(self.env)
        try:
            proc.run(PUT, '/testmapping4')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)

        try:
            proc.run(POST, '/testmapping4')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)

        try:
            proc.run(DELETE, '/testmapping4')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_notImplementedMethods(self):
        """
        Not implemented methods should raise an error.
        """
        proc = Processor(self.env)
        try:
            proc.run('MUH', '/testmapping4')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)

        try:
            proc.run('KUH', '/testmapping4')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_ALLOWED)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapperTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_tree.py
# Compiled at: 2010-12-23 17:42:41
"""
A test suite for a ResourceTree resource.
"""
from seishub.core.exceptions import SeisHubError
from seishub.core.processor import GET, Processor, DELETE, MOVE, PUT, POST
from seishub.core.processor.resources import Resource
from seishub.core.processor.resources.rest import RESTFolder, RESTPackageFolder, RESTResourceTypeFolder
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import unittest

class ATestResource(Resource):
    """
    A test resource.
    """

    def __init__(self, text):
        Resource.__init__(self)
        self.is_leaf = True
        self.text = text

    def render_GET(self, request):
        return 'Hello %s!' % self.text


class ResourceTreeTests(SeisHubEnvironmentTestCase):
    """
    A test suite for a ResourceTree resource.
    """

    def test_getRoot(self):
        proc = Processor(self.env)
        data = proc.run(GET, '/')
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('xml' in data.keys())

    def test_addChild(self):
        self.env.tree.putChild('/test/muh/muh', ATestResource('maeh'))
        self.env.tree.putChild('/test/muh/kuh', ATestResource('muh'))
        self.env.tree.putChild('maeh', ATestResource('you'))
        self.env.tree.putChild('test2', ATestResource('again'))
        proc = Processor(self.env)
        data = proc.run(GET, '/')
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('maeh' in data)
        self.assertTrue('test' in data)
        self.assertTrue('test2' in data)
        data = proc.run(GET, '/test')
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('muh' in data)
        data = proc.run(GET, '/test/muh')
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('kuh' in data)
        self.assertTrue('muh' in data)
        data = proc.run(GET, '/test/muh/kuh')
        self.assertEquals('Hello muh!', data)
        data = proc.run(GET, '/maeh')
        self.assertEquals('Hello you!', data)
        data = proc.run(GET, '/test2')
        self.assertEquals('Hello again!', data)
        data = proc.run(GET, '/test/muh/muh')
        self.assertEquals('Hello maeh!', data)

    def test_overwritingResourceTree(self):
        self.env.tree.putChild('/test/muh/kuh/blub', ATestResource('World'))
        self.env.tree.putChild('/test/muh/muh/stub', ATestResource('muh'))
        self.env.tree.putChild('/test/muh', ATestResource('maeh'))
        proc = Processor(self.env)
        data = proc.run(GET, '/test')
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('muh' in data)
        self.assertEqual(len(data), 1)
        data = proc.run(GET, '/test/muh')
        self.assertTrue(isinstance(data, basestring))

    def test_invalidMethods(self):
        proc = Processor(self.env)
        for method in ['MUH', 'XXX', 'GETPUT']:
            try:
                proc.run(method, '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_forbiddenMethods(self):
        proc = Processor(self.env)
        for method in [POST, PUT, DELETE, MOVE]:
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

    def test_someRESTResourceTypes(self):
        proc = Processor(self.env)
        result = proc.run(GET, '/')
        self.assertTrue(isinstance(result.get('xml'), RESTFolder))
        result = proc.run(GET, '/xml')
        self.assertTrue(isinstance(result.get('seishub'), RESTPackageFolder))
        result = proc.run(GET, '/xml/seishub')
        self.assertTrue(isinstance(result.get('stylesheet'), RESTResourceTypeFolder))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResourceTreeTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/bestappever/tests.py
# Compiled at: 2008-08-25 05:22:59
import unittest

class ViewTests(unittest.TestCase):

    def setUp(self):
        self._cleanup()
        import bestappever, zope.configuration.xmlconfig
        zope.configuration.xmlconfig.file('configure.zcml', package=bestappever)

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        from zope.testing.cleanup import cleanUp
        cleanUp()

    def test_my_view(self):
        from bestappever.views import my_view
        context = DummyContext()
        request = DummyRequest()
        result = my_view(context, request)
        self.assertEqual(result.status, '200 OK')
        body = result.app_iter[0]
        self.failUnless('Welcome to bestappever' in body)
        self.assertEqual(len(result.headerlist), 2)
        self.assertEqual(result.headerlist[0], ('content-type', 'text/html; charset=UTF-8'))
        self.assertEqual(result.headerlist[1], ('Content-Length',
         str(len(body))))


class DummyContext:
    pass


class DummyRequest:
    pass
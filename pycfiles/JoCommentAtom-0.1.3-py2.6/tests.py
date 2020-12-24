# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jocommentatom/tests.py
# Compiled at: 2011-01-14 13:52:45
import unittest
from pyramid.configuration import Configurator
from pyramid import testing

class TestNotFoundView(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def test_redirect(self):
        from jocommentatom.views import notfound_view
        request = testing.DummyRequest()
        response = notfound_view(request)
        self.assertEqual(response.status, '301 Moved Permanently')
        self.failUnless(('Location', '/') in response.headerlist)
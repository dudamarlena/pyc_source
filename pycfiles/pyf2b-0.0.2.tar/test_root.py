# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/tests/functional/test_root.py
# Compiled at: 2010-10-13 09:43:04
__doc__ = '\nFunctional test suite for the root controller.\n\nThis is an example of how functional tests can be written for controllers.\n\nAs opposed to a unit-test, which test a small unit of functionality,\nfunctional tests exercise the whole application and its WSGI stack.\n\nPlease read http://pythonpaste.org/webtest/ for more information.\n\n'
from nose.tools import assert_true
from pyf.services.tests import TestController

class TestRootController(TestController):

    def test_index(self):
        response = self.app.get('/')
        assert_true('DashBoard' in response)
        assert_true('PyF' in response)
        assert_true('Login' in response)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/tests/functional/test_root.py
# Compiled at: 2010-10-13 09:43:04
"""
Functional test suite for the root controller.

This is an example of how functional tests can be written for controllers.

As opposed to a unit-test, which test a small unit of functionality,
functional tests exercise the whole application and its WSGI stack.

Please read http://pythonpaste.org/webtest/ for more information.

"""
from nose.tools import assert_true
from pyf.services.tests import TestController

class TestRootController(TestController):

    def test_index(self):
        response = self.app.get('/')
        assert_true('DashBoard' in response)
        assert_true('PyF' in response)
        assert_true('Login' in response)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyaler/tests.py
# Compiled at: 2010-07-24 11:44:38
import os, pyaler
from webtest import TestApp
import unittest
config = os.path.join(os.path.dirname(pyaler.__file__), 'tests.yaml')

class TestPyaler(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(pyaler.make_app({}, config=config))

    def test_reset(self):
        resp = self.app.get('/arduinos/reset')
        resp.mustcontain('OK')


class TestPyalerExtension(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(pyaler.make_app({}, config=config, app='test_app'))

    def test_index(self):
        resp = self.app.get('/')
        resp.mustcontain('<title>')
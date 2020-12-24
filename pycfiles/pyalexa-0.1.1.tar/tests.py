# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
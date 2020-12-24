# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/bricklayer/testsuite/generatetest.py
# Compiled at: 2013-11-21 19:28:55
from django.test import TestCase
from bricklayer.utils import *
import test_app, os, imp

class GenerateTestTestCase(TestCase):

    def setUp(self):
        self.app_path = os.path.abspath(test_app.__path__[0])
        with open(os.path.join(self.app_path, 'tests.py')) as (f):
            self.tests_content = f.read()
        run_manage_py('generatetest tset test_app')

    def test_file_exists(self):
        self.assertTrue(exists_path(self.app_path, 'testsuite', 'tset.py'))

    def test_init_text(self):
        with open(os.path.join(self.app_path, 'testsuite', '__init__.py')) as (f):
            test_file = f.read()
        self.assertIn('\nfrom test_app.testsuite.tset import *', test_file)

    def test_test_text(self):
        with open(os.path.join(self.app_path, 'testsuite', 'tset.py')) as (f):
            test_file = f.read()
        self.assertIn('from django.test import TestCase', test_file)
        self.assertIn('class TsetTestCase(TestCase):', test_file)

    def tearDown(self):
        self.app_path = os.path.abspath(test_app.__path__[0])
        with open(os.path.join(self.app_path, 'tests.py'), 'w') as (f):
            f.write(self.tests_content)
        for file in os.listdir(os.path.join(self.app_path, 'testsuite')):
            os.remove(os.path.join(self.app_path, 'testsuite', file))

        os.rmdir(os.path.join(self.app_path, 'testsuite'))
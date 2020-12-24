# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/bricklayer/testsuite/generateform.py
# Compiled at: 2013-11-21 19:28:55
from django.test import TestCase
from bricklayer.utils import run_manage_py, exists_path
import test_app, os, imp

class GenerateFormTestCase(TestCase):

    def setUp(self):
        self.app_path = os.path.abspath(test_app.__path__[0])
        run_manage_py('generateform test_app -m TestModel')

    def test_file_creation(self):
        self.assertTrue(exists_path(self.app_path, 'forms.py'))

    def test_form(self):
        forms = dir(imp.load_source('forms', os.path.join(self.app_path, 'forms.py')))
        self.assertIn('TestModelForm', forms)

    def tearDown(self):
        os.remove(os.path.join(self.app_path, 'forms.py'))
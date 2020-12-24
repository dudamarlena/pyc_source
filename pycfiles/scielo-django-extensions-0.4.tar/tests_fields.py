# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gustavofonseca/prj/github/scielo-django-extensions/scielo_extensions/tests/tests_fields.py
# Compiled at: 2012-10-08 09:47:25
from django import forms
from django.test import TestCase
from scielo_extensions import formfields

class ISSNFieldTest(TestCase):
    VALID_ISSNS = [
     '1678-5320', '0044-5967', '0102-8650', '2179-975X',
     '1413-7852', '0103-2100']
    INVALID_ISSNS = ['A123-4532', '1t23-8979', '0900-090900', '9827-u982',
     '8992-8u77', '1111-111Y']

    def setUp(self):

        class Baz(forms.Form):
            print_issn = formfields.ISSNField()

        self.BazForm = Baz

    def test_valid_data(self):
        for issn in self.VALID_ISSNS:
            form = self.BazForm({'print_issn': issn})
            self.assertTrue(form.errors.get('print_issn') is None)

        return

    def test_invalid_data(self):
        for issn in self.INVALID_ISSNS:
            form = self.BazForm({'print_issn': issn})
            self.assertEqual(form.errors.get('print_issn')[0], 'Enter a valid ISSN.')
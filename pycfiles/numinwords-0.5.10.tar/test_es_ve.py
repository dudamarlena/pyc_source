# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_es_ve.py
# Compiled at: 2020-04-17 01:12:44
from __future__ import unicode_literals
from numinwords import numinwords
from . import test_es
TEST_CASES_TO_CURRENCY = (
 (1, 'un bolívar'),
 (2, 'dos bolívares'),
 (8, 'ocho bolívares'),
 (12, 'doce bolívares'),
 (21, 'veintiun bolívares'),
 (81.25, 'ochenta y un bolívares y veinticinco centavos'),
 (100, 'cien bolívares'))

class numinwordsESVETest(test_es.numinwordsESTest):

    def test_number(self):
        for test in test_es.TEST_CASES_CARDINAL:
            self.assertEqual(numinwords(test[0], lang=b'es_VE'), test[1])

    def test_ordinal(self):
        for test in test_es.TEST_CASES_ORDINAL:
            self.assertEqual(numinwords(test[0], lang=b'es_VE', ordinal=True), test[1])

    def test_ordinal_num(self):
        for test in test_es.TEST_CASES_ORDINAL_NUM:
            self.assertEqual(numinwords(test[0], lang=b'es', to=b'ordinal_num'), test[1])

    def test_currency(self):
        for test in TEST_CASES_TO_CURRENCY:
            self.assertEqual(numinwords(test[0], lang=b'es_VE', to=b'currency', old=True), test[1])
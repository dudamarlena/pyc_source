# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_es_ni.py
# Compiled at: 2020-04-17 01:12:41
from __future__ import unicode_literals
from numinwords import numinwords
from . import test_es
TEST_NIO = (
 (1.0, 'un córdoba con cero centavos'),
 (2.0, 'dos córdobas con cero centavos'),
 (8.0, 'ocho córdobas con cero centavos'),
 (12.0, 'doce córdobas con cero centavos'),
 (21.0, 'veintiun córdobas con cero centavos'),
 (81.25, 'ochenta y un córdobas con veinticinco centavos'),
 (100.0, 'cien córdobas con cero centavos'))

class numinwordsESNITest(test_es.numinwordsESTest):

    def test_currency(self):
        for test in TEST_NIO:
            self.assertEqual(numinwords(test[0], lang=b'es_NI', to=b'currency'), test[1])
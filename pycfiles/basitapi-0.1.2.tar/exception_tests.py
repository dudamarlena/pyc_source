# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/DjangoProjects/basitapi/basitapi/tests/exception_tests.py
# Compiled at: 2013-01-16 01:28:35
from django.test import TestCase
from basitapi.exception import ApiException

class ExceptionTest(TestCase):

    def test_init(self):
        exception = ApiException('Hata', 500, application_code=1000)
        self.assertEqual(exception.message, 'Hata')
        self.assertEqual(exception.status, 500)
        self.assertEqual(exception.application_code, 1000)
# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ddanier/work/django/django_price/tests/test_smoke.py
# Compiled at: 2015-09-08 22:28:09
from django.test import TestCase

class ModelAPITest(TestCase):

    def test_smoke(self):
        """Just some basic smoke tests (syntax, app loading)"""
        import django_price, django_price.currency, django_price.fields, django_price.forms, django_price.models, django_price.price, django_price.tax, django_price.utils
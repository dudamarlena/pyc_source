# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/tests/test_decorators.py
# Compiled at: 2017-11-28 02:59:59
import warnings
from django.test import TestCase
from formfactory.decorators import generic_deprecation

class DeprecationTestCase(TestCase):

    def test_generic_deprecation(self):
        with warnings.catch_warnings(record=True) as (w):
            warnings.simplefilter('always')

            @generic_deprecation('generic_deprecation_message')
            def wrapped_method():
                pass

            wrapped_method()
            assert len(w) == 1
            assert issubclass(w[(-1)].category, DeprecationWarning)
            assert 'generic_deprecation_message' in str(w[(-1)].message)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-tisqp5jr/django-currencyware/currencyware/tests/tests.py
# Compiled at: 2018-08-22 09:57:42
# Size of source mod 2**32: 1606 bytes
import time
from django.test import TestCase
from django.conf import settings
from django.utils import translation
from django.core.management import call_command
from currencyware.currency import get_all_currencies
from currencyware.currency import get_all_currencies_sorted
from currencyware.currency import get_all_currencies_prioritized
from currencyware.currency import get_display
from currencyware import defaults as defs

class TestCountryCase(TestCase):
    __doc__ = '\n    Country Test\n    '

    def setUp(self):
        pass

    def test_xlate_display(self):
        name = get_display('AED')
        self.assertEquals(name, 'UAE Dirham')

    def test_xlate_priority(self):
        translation.activate('zh-hant')
        name = get_display('AED')
        self.assertEquals(name, '阿拉伯聯合大公國迪拉姆')

    def test_xlate_en_unsorted(self):
        translation.activate('en')
        currencies = get_all_currencies()
        self.assertEquals(currencies[0][1], 'UAE Dirham')

    def test_xlate_en_sorted(self):
        translation.activate('en')
        currencies = get_all_currencies_sorted()
        self.assertEquals(currencies[0][1], 'Afghani')

    def test_xlate_en_prioritized(self):
        translation.activate('en')
        currencies = get_all_currencies_prioritized()
        self.assertEquals(currencies[0][1], 'Canadian Dollar')

    def test_xlate_fa_prioritized(self):
        translation.activate('fr')
        currencies = get_all_currencies_prioritized()
        self.assertEquals(currencies[0][1], 'Dollar canadien')
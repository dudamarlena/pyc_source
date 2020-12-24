# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-tisqp5jr/django-currencyware/currencyware/currency.py
# Compiled at: 2018-08-22 09:57:42
# Size of source mod 2**32: 2012 bytes
import locale, functools
from django.utils import translation
from django.utils.translation import ugettext as _
from . import defaults as defs
from .utils import get_cache_key, get_from_cache, set_to_cache

def get_display(code):
    display = _('ISO_4217.' + code)
    return display


def get_currencies(codes):
    """ Returns a list of (code, translation) tuples for codes  """
    currencies = [(code, get_display(code)) for code in codes]
    return currencies


def get_all_currencies(codes=defs.ALL_CURRENCY_CODES):
    """ Returns a list of (code, translation) tuples for all currency codes  """
    key = get_cache_key(codes)
    currencies = get_from_cache(key)
    if currencies:
        return currencies
    else:
        currencies = get_currencies(codes)
        set_to_cache(key, currencies)
        return currencies


def get_all_currencies_sorted(codes=defs.ALL_CURRENCY_CODES):
    """ Returns a list of (code, translation) tuples for all currency codes  """
    key = get_cache_key(codes, True)
    currencies = get_from_cache(key)
    if currencies:
        return currencies
    else:
        currencies = sorted((get_currencies(codes)),
          key=(functools.cmp_to_key(lambda a, b: locale.strcoll(a[1], b[1]))))
        set_to_cache(key, currencies)
        return currencies


def get_all_currencies_prioritized(priority_codes=defs.PRIORITY_CURRENCY_CODES, codes=defs.ALL_CURRENCY_CODES):
    """ Returns a sorted list of (code, translation) tuples for currency codes  """
    codes_subset = list(set(codes) - set(priority_codes))
    key = get_cache_key(priority_codes + codes_subset, True)
    currencies = get_from_cache(key)
    if currencies:
        return currencies
    else:
        currencies = get_from_cache(key)
        priority_currencies = get_all_currencies(priority_codes)
        currencies = get_all_currencies_sorted(codes_subset)
        combined_currencies = priority_currencies + currencies
        set_to_cache(key, combined_currencies)
        return combined_currencies
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/d2w/apps/django-countryware/countryware/country.py
# Compiled at: 2018-07-09 16:47:03
# Size of source mod 2**32: 1566 bytes
import locale, functools
from django.utils import translation
from django.utils.translation import ugettext as _
from . import defaults as defs
from .utils import memorize
_cache_countries = {}
_cache_countries_sorted = {}
_cache_countries_sorted_prioritized = {}

def get_display(code):
    display = _('ISO_3166-1.' + code)
    return display


def get_countries(codes):
    """ Returns a list of (code, translation) tuples for codes  """
    countries = [(code, get_display(code)) for code in codes]
    return countries


@memorize(_cache_countries)
def get_all_countries(codes=defs.ALL_COUNTRY_CODES):
    """ Returns a list of (code, translation) tuples for all country codes  """
    countries = get_countries(codes)
    return countries


@memorize(_cache_countries_sorted)
def get_all_countries_sorted(codes=defs.ALL_COUNTRY_CODES):
    """ Returns a list of (code, translation) tuples for all country codes  """
    countries = sorted((get_countries(codes)),
      key=(functools.cmp_to_key(lambda a, b: locale.strcoll(a[1], b[1]))))
    return countries


@memorize(_cache_countries_sorted_prioritized)
def get_all_countries_prioritized(priority_codes=defs.PRIORITY_COUNTRY_CODES, codes=defs.ALL_COUNTRY_CODES):
    """ Returns a sorted list of (code, translation) tuples for codes  """
    prioritized = []
    if priority_codes:
        if len(priority_codes) > 0:
            prioritized = get_countries(priority_codes)
    countries = get_all_countries(codes)
    return prioritized + countries
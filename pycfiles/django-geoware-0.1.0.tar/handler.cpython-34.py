# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/management/utils/handler.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 1284 bytes
import logging
from ... import defaults as defs
logger = logging.getLogger('geoware.utils.fixer')

def country_custom_handler(country):
    """
    Manages special cases on a country object.
    """
    if not country.jurisdiction:
        country.jurisdiction = country


def division_custom_handler(division):
    """
    Manages special cases on a division object.
    """
    canadian_province_code = 'ca' in division.fips.split('.')[0].lower()
    if canadian_province_code:
        code = defs.GEOWARE_CANADA_PROVINCE_CODES.get('division.code')
        if code:
            division.code = code


def subdivision_custom_handler(subdivision):
    """
    Manages special cases on a subdivision object.
    """
    pass


def city_custom_handler(city):
    """
    Manages special cases on a city object.
    """
    pass


def language_custom_handler(language):
    """
    Manages special cases on a language object.
    """
    pass


def timezone_custom_handler(timezone):
    """
    Manages special cases on a timezone object.
    """
    pass


def currency_custom_handler(currency):
    """
    Manages special cases on a currency object.
    """
    pass


def altname_custom_handler(currency):
    """
    Manages special cases on an altname object.
    """
    pass
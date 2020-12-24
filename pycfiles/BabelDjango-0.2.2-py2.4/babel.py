# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/babeldjango/templatetags/babel.py
# Compiled at: 2008-06-18 11:34:43
from django.conf import settings
from django.template import Library
from django.utils.translation import to_locale
try:
    from pytz import timezone
except ImportError:
    timezone = None

from babeldjango.middleware import get_current_locale
babel = __import__('babel', {}, {}, ['core', 'support'])
Format = babel.support.Format
Locale = babel.core.Locale
register = Library()

def _get_format():
    locale = get_current_locale()
    if not locale:
        locale = Locale.parse(to_locale(settings.LANGUAGE_CODE))
    if timezone:
        tzinfo = timezone(settings.TIME_ZONE)
    else:
        tzinfo = None
    return Format(locale, tzinfo)


def datefmt(date=None, format='medium'):
    return _get_format().date(date, format=format)


datefmt = register.filter(datefmt)

def datetimefmt(datetime=None, format='medium'):
    return _get_format().datetime(datetime, format=format)


datetimefmt = register.filter(datetimefmt)

def timefmt(time=None, format='medium'):
    return _get_format().time(time, format=format)


timefmt = register.filter(timefmt)

def numberfmt(number):
    return _get_format().number(number)


numberfmt = register.filter(numberfmt)

def decimalfmt(number, format=None):
    return _get_format().decimal(number, format=format)


decimalfmt = register.filter(decimalfmt)

def currencyfmt(number, currency):
    return _get_format().currency(number, currency)


currencyfmt = register.filter(currencyfmt)

def percentfmt(number, format=None):
    return _get_format().percent(number, format=format)


percentfmt = register.filter(percentfmt)

def scientificfmt(number):
    return _get_format().scientific(number)


scientificfmt = register.filter(scientificfmt)
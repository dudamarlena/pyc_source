# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/formattings/humanize/number.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 4615 bytes
"""Humanizing functions for numbers."""
import re
from fractions import Fraction
from . import compat
from .i18n import gettext as _, gettext_noop as N_, pgettext as P_

def ordinal(value):
    """Converts an integer to its ordinal as a string. 1 is '1st', 2 is '2nd',
    3 is '3rd', etc. Works for any integer or anything int() will turn into an
    integer.  Anything other value will have nothing done to it."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    else:
        t = (
         P_('0', 'th'),
         P_('1', 'st'),
         P_('2', 'nd'),
         P_('3', 'rd'),
         P_('4', 'th'),
         P_('5', 'th'),
         P_('6', 'th'),
         P_('7', 'th'),
         P_('8', 'th'),
         P_('9', 'th'))
        if value % 100 in (11, 12, 13):
            return '%d%s' % (value, t[0])
        return '%d%s' % (value, t[(value % 10)])


def intcomma(value, seperator=','):
    """Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.  To maintain
    some compatability with Django's intcomma, this function also accepts
    floats."""
    try:
        if isinstance(value, compat.string_types):
            float(value.replace(seperator, ''))
        else:
            float(value)
    except (TypeError, ValueError):
        return value
    else:
        orig = str(value)
        new = re.sub('^(-?\\d+)(\\d{3})', '\\g<1>' + seperator + '\\g<2>', orig)
        if orig == new:
            return new
        return intcomma(new, seperator)


powers = [10 ** x for x in (6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
human_powers = (N_('million'), N_('billion'), N_('trillion'), N_('quadrillion'),
 N_('quintillion'), N_('sextillion'), N_('septillion'),
 N_('octillion'), N_('nonillion'), N_('decillion'), N_('googol'))

def intword(value, format='%.1f'):
    """Converts a large integer to a friendly text representation. Works best for
    numbers over 1 million. For example, 1000000 becomes '1.0 million', 1200000
    becomes '1.2 million' and '1200000000' becomes '1.2 billion'.  Supports up to
    decillion (33 digits) and googol (100 digits).  You can pass format to change
    the number of decimal or general format of the number portion.  This function
    returns a string unless the value passed was unable to be coaxed into an int."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    else:
        if value < powers[0]:
            return str(value)
        for ordinal, power in enumerate(powers[1:], 1):
            if value < power:
                chopped = value / float(powers[(ordinal - 1)])
                return (' '.join([format, _(human_powers[(ordinal - 1)])]) % chopped).encode('utf-8')

        return str(value)


def apnumber(value):
    """For numbers 1-9, returns the number spelled out. Otherwise, returns the
    number. This follows Associated Press style.  This always returns a string
    unless the value was not int-able, unlike the Django filter."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    else:
        if not 0 < value < 10:
            return str(value)
            return (_('one'), _('two'), _('three'), _('four'), _('five'), _('six'),
             _('seven'), _('eight'), _('nine'))[(value - 1)]


def fractional(value):
    """
    There will be some cases where one might not want to show
        ugly decimal places for floats and decimals.
    This function returns a human readable fractional number
        in form of fractions and mixed fractions.
    Pass in a string, or a number or a float, and this function returns
        a string representation of a fraction
        or whole number
        or a mixed fraction
    Examples:
        fractional(0.3) will return '1/3'
        fractional(1.3) will return '1 3/10'
        fractional(float(1/3)) will return '1/3'
        fractional(1) will return '1'
    This will always return a string.
    """
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    else:
        wholeNumber = int(number)
        frac = Fraction(number - wholeNumber).limit_denominator(1000)
        numerator = frac._numerator
        denominator = frac._denominator
        if wholeNumber:
            if not numerator:
                if denominator == 1:
                    return '%.0f' % wholeNumber
        if not wholeNumber:
            return '%.0f/%.0f' % (numerator, denominator)
        return '%.0f %.0f/%.0f' % (wholeNumber, numerator, denominator)
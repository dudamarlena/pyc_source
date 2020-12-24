# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/checksums.py
# Compiled at: 2018-07-11 18:15:30
"""
Common checksum routines (used in multiple localflavor/ cases, for example).
"""
__all__ = [
 'luhn']
from django.utils import six
LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)

def luhn(candidate):
    """
    Checks a candidate number for validity according to the Luhn
    algorithm (used in validation of, for example, credit cards).
    Both numeric and string candidates are accepted.
    """
    if not isinstance(candidate, six.string_types):
        candidate = str(candidate)
    try:
        evens = sum([ int(c) for c in candidate[-1::-2] ])
        odds = sum([ LUHN_ODD_LOOKUP[int(c)] for c in candidate[-2::-2] ])
        return (evens + odds) % 10 == 0
    except ValueError:
        return False
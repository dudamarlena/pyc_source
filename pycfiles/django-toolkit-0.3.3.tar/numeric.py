# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/numeric.py
# Compiled at: 2013-11-26 18:51:11
from decimal import Decimal

def zero_if_none(value):
    if not value:
        return Decimal('0')
    return value


def percentage_change(first, second):
    if first in (None, 0) or second in (None, 0):
        return
    return (Decimal(second) - Decimal(first)) / Decimal(first) * 100
    return
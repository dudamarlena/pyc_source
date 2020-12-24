# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/validators.py
# Compiled at: 2017-10-08 17:55:08
"""
"""
from __future__ import absolute_import, print_function, unicode_literals
import datetime, numbers, six
from .exceptions import ValidationError
from future.utils import raise_with_traceback

def check_length(value, min_length=None, max_length=None):
    if min_length and len(value) < min_length:
        raise ValidationError((b'{} is too short. Min length is {}').format(value, min_length))
    if max_length and len(value) > max_length:
        raise ValidationError((b'{} is too long. Max length is {}').format(value, max_length))
    return value


def is_datetime(value):
    if not isinstance(value, datetime.datetime):
        raise ValidationError(b'Expected a datetime object.')
    return value


def is_date(value):
    if not isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
        raise ValidationError(b'Expected a date object.')
    return value


def is_bool(value):
    if not isinstance(value, bool):
        raise ValidationError(b'Expected a bool object.')
    return value


def is_set(value):
    if not isinstance(value, set):
        raise ValidationError(b'Expected a set object.')
    return value


def is_dict(value):
    if not isinstance(value, dict):
        raise ValidationError(b'Expected a dict object.')
    return value


def is_list(value):
    if not isinstance(value, (list, tuple)):
        raise ValidationError(b'Expected a list or tuple object.')
    return value


def is_int(value):
    msg = b'Expected an int object.'
    if isinstance(value, six.string_types) and not value.isdigit():
        raise ValidationError(msg)
    elif not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(msg)
    return value


def is_float(value):
    if not isinstance(value, float):
        raise ValidationError(b'Expected a float object.')
    return value


def is_number(value):
    if not isinstance(value, numbers.Number) or isinstance(value, bool):
        raise ValidationError((b'{}, must be a number.').format(value))
    return value


def is_char(value):
    if not isinstance(value, six.string_types):
        raise ValidationError(b'Expected a char object.')
    return value
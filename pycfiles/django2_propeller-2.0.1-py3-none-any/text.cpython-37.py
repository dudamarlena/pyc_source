# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Development\django2-propeller\django2_propeller\text.py
# Compiled at: 2019-04-26 08:32:14
# Size of source mod 2**32: 714 bytes
from __future__ import unicode_literals
try:
    from django.utils.encoding import force_text
except ImportError:
    import django.utils.encoding as force_text

def text_value(value):
    """
    Force a value to text, render None as an empty string
    """
    if value is None:
        return ''
    return force_text(value)


def text_concat(*args, **kwargs):
    """
    Concatenate several values as a text string with an optional separator
    """
    separator = text_value(kwargs.get('separator', ''))
    values = filter(None, [text_value(v) for v in args])
    return separator.join(values)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/text.py
# Compiled at: 2017-02-17 12:55:03
from __future__ import unicode_literals
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

def text_value(value):
    """
    Force a value to text, render None as an empty string
    """
    if value is None:
        return b''
    else:
        return force_text(value)


def text_concat(*args, **kwargs):
    """
    Concatenate several values as a text string with an optional separator
    """
    separator = text_value(kwargs.get(b'separator', b''))
    values = filter(None, [ text_value(v) for v in args ])
    return separator.join(values)
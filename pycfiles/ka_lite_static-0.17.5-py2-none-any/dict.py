# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/utils/dict.py
# Compiled at: 2018-07-11 18:15:32
from django.utils import six
from django.utils.encoding import smart_bytes

def dict_strip_unicode_keys(uni_dict):
    """
    Converts a dict of unicode keys into a dict of ascii keys.

    Useful for converting a dict to a kwarg-able format.
    """
    if six.PY3:
        return uni_dict
    return dict([ (smart_bytes(key), value) for key, value in uni_dict.items() ])
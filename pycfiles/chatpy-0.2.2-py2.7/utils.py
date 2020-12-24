# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\utils.py
# Compiled at: 2015-01-11 13:52:03
import six

def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json
        except ImportError:
            try:
                from django.utils import simplejson as json
            except ImportError:
                raise ImportError("Can't load a json library")

    return json


def convert_to_utf8_str(arg):
    if isinstance(arg, six.text_type):
        return arg
    arg = six.text_type(arg).encode('utf-8')
    return arg
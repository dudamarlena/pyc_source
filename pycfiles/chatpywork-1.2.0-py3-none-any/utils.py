# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
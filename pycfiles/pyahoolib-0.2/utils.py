# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyahooapis\utils.py
# Compiled at: 2011-04-21 00:28:38


def import_json():
    try:
        import json
        return json
    except:
        try:
            import simplejson
            return simplejson
        except:
            import django.utils.simplejson
            return django.utils.simplejson
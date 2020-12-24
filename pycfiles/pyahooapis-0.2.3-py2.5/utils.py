# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
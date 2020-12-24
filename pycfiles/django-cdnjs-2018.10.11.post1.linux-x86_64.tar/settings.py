# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cdnjs/settings.py
# Compiled at: 2018-10-11 09:01:15
from django.conf import settings

class Settings(object):
    """
    Module settings helper.
    """
    prefix = 'CDNJS_'

    @staticmethod
    def get(key, default=None):
        key = ('{}{}').format(Settings.prefix, key)
        if not hasattr(settings, key):
            return default
        return getattr(settings, key)
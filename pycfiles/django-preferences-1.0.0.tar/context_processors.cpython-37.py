# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/context_processors.py
# Compiled at: 2018-12-20 02:32:17
# Size of source mod 2**32: 223 bytes
from preferences import preferences

def preferences_cp(request):
    """
    Adds preferences to template context when used
    through TEMPLATE_CONTEXT_PROCESSORS setting.
    """
    return {'preferences': preferences}
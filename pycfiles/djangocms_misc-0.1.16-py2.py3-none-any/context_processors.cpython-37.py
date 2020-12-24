# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/context_processors.py
# Compiled at: 2018-07-27 08:00:56
# Size of source mod 2**32: 401 bytes
from __future__ import unicode_literals
from django.conf import settings

def get_env(request):
    """
    expose is_live/stage/dev and SITE_ID to context
    """
    context = {'SITE_ID': settings.SITE_ID}
    env = getattr(settings, 'ENV', None)
    if env:
        context.update({'ENV': settings.ENV, 
         'is_' + str(env): True})
    return context
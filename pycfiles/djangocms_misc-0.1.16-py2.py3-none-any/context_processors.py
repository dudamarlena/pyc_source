# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/context_processors.py
# Compiled at: 2018-07-27 08:00:56
from __future__ import unicode_literals
from django.conf import settings

def get_env(request):
    """
    expose is_live/stage/dev and SITE_ID to context
    """
    context = {b'SITE_ID': settings.SITE_ID}
    env = getattr(settings, b'ENV', None)
    if env:
        context.update({b'ENV': settings.ENV, 
           b'is_' + str(env): True})
    return context
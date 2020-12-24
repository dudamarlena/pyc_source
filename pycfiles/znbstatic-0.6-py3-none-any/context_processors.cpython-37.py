# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/znbstatic/znbstatic/context_processors.py
# Compiled at: 2019-01-07 16:14:59
# Size of source mod 2**32: 519 bytes
from django.conf import settings

def static_urls(request):
    """
    Adds value from ZNBSTATIC_VERSION to context.

    Add 'znbstatic.context_processors.static_urls' to the corresponding engine in
    OPTIONS.context_processors in settings.TEMPLATES, and then
    set ZNBSTATIC_VERSION and you can include {{ static_version }} in the template or use it from
    the context in a template tag.
    """
    static_version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
    return {'static_version': static_version}
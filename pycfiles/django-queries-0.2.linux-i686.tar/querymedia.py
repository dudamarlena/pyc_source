# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/queries/templatetags/querymedia.py
# Compiled at: 2010-05-22 03:01:05
from django.template import Library
register = Library()

def query_media_prefix():
    """
    Returns the string contained in the setting query_MEDIA_PREFIX.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    else:
        try:
            return settings.QUERY_MEDIA_PREFIX
        except:
            return settings.ADMIN_MEDIA_PREFIX


query_media_prefix = register.simple_tag(query_media_prefix)
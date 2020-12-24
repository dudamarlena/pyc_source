# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\context_processors.py
# Compiled at: 2013-08-27 09:18:22
from __future__ import unicode_literals
from django.conf import settings
from django.utils import dateformat

def analytics(request):
    return {b'ga_tracking_id': getattr(settings, b'GA_TRACKING_ID', b''), 
       b'ga_tracking_domain': getattr(settings, b'GA_TRACKING_DOMAIN', b'')}


def version_string(request):
    revision_hash = getattr(settings, b'REVISION_HASH', b'')
    revision_date = getattr(settings, b'REVISION_DATE', b'')
    if revision_date:
        try:
            revision_date = dateformat.format(revision_date, b'j M, G:i')
        except:
            revision_date = b''

    revision_env = getattr(settings, b'REVISION_ENV', b'')
    if revision_env:
        revision_env = b', ' + revision_env
    if revision_hash and revision_date:
        version = (b'v. {} ({}{})').format(revision_date, revision_hash, revision_env)
    else:
        version = b''
    return {b'VERSION_STRING': version}
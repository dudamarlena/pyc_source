# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Updoc/updoc/context_processors.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 705 bytes
from django.conf import settings
from updoc import __version__
from updoc.models import LastDocs, ProxyfiedHost, RssRoot
__author__ = 'Matthieu Gallet'

def most_checked(request):
    user = request.user if request.user.is_authenticated else None
    most_checked_ = LastDocs.query(request).select_related('doc').order_by('-count')[0:5]
    if not settings.PUBLIC_INDEX:
        if user is None:
            most_checked_ = []
    has_proxyfied_hosts = ProxyfiedHost.objects.all().count() > 0
    has_rss_hosts = RssRoot.objects.all().count() > 0
    return {'updoc_most_checked':most_checked_,  'updoc_version':__version__,  'has_proxyfied_hosts':has_proxyfied_hosts, 
     'has_rss_hosts':has_rss_hosts}
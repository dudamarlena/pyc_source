# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/panya/context_processors.py
# Compiled at: 2011-05-26 02:47:52
from django.contrib.sites.models import Site

def site(request):
    try:
        site = Site.objects.get_current()
    except Site.DoesNotExist:
        site = None

    return {'site': site}
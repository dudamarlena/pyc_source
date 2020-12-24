# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/context_processors.py
# Compiled at: 2019-04-03 22:56:25
# Size of source mod 2**32: 399 bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject

def site(request):
    site = SimpleLazyObject(lambda : get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'
    return {'site':site, 
     'site_root':SimpleLazyObject(lambda : '{0}://{1}'.format(protocol, site.domain))}
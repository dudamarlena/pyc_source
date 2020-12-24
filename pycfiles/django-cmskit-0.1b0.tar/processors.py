# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/processors.py
# Compiled at: 2012-11-19 10:50:40
from django.conf import settings
from django.contrib.sites.models import Site

def site(request):
    site = Site.objects.get_current()
    return {'SITE_NAME': getattr(settings, 'SITE_NAME', site.name), 
       'SITE_DOMAIN': getattr(settings, 'SITE_DOMAIN', site.domain)}
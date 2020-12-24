# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/themes/context_processors.py
# Compiled at: 2013-01-28 01:22:56
import simplejson
from django.conf import settings
from django.contrib.sites.models import get_current_site

def static(request):
    site_theme = settings.THEME
    static_theme_url = '%sthemes/%s/static/' % (settings.STATIC_URL, site_theme)
    static_common_url = '%sthemes/common/static/' % settings.STATIC_URL
    return {'site': get_current_site(request), 
       'GOSCALE_THEME': site_theme, 
       'STATIC_THEME_URL': static_theme_url, 
       'STATIC_COMMON_URL': static_common_url}
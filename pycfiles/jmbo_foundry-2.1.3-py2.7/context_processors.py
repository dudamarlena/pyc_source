# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/context_processors.py
# Compiled at: 2016-03-12 03:16:37
from django.contrib.sites.models import get_current_site
from django.conf import settings
from foundry.utils import get_preference

def foundry(request):
    return {'FOUNDRY': settings.FOUNDRY, 
       'LAYER_PATH': settings.LAYERS['layers'][(-1)] + '/', 
       'CURRENT_SITE': get_current_site(request), 
       'ANALYTICS_TAGS': get_preference('GeneralPreferences', 'analytics_tags'), 
       'SITE_DESCRIPTION': get_preference('GeneralPreferences', 'site_description'), 
       'FOUNDRY_HAS_FACEBOOK_CONNECT': getattr(settings, 'FACEBOOK_APP_ID', '') != '', 
       'FOUNDRY_HAS_TWITTER_OAUTH': getattr(settings, 'TWITTER_CONSUMER_KEY', '') != '', 
       'FOUNDRY_HAS_GOOGLE_OAUTH2': getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID', '') != '', 
       'FOUNDRY_HAS_GALLERY': 'gallery' in settings.INSTALLED_APPS, 
       'FOUNDRY_HAS_BANNER': 'banner' in settings.INSTALLED_APPS}
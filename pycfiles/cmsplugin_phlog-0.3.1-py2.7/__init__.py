# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/cmsplugin_phlog/__init__.py
# Compiled at: 2013-06-26 16:38:22
from django.conf import settings
if 'cmsplugin_phlog' in settings.INSTALLED_APPS:
    if not hasattr(settings, 'CMS_PLUGIN_PHLOG_MEDIA_URL'):
        settings.CMS_PLUGIN_PHLOG_MEDIA_URL = settings.MEDIA_URL + 'cmsplugin_phlog/'
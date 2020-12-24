# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/cmsplugin_phlog/__init__.py
# Compiled at: 2013-06-26 16:38:22
from django.conf import settings
if 'cmsplugin_phlog' in settings.INSTALLED_APPS:
    if not hasattr(settings, 'CMS_PLUGIN_PHLOG_MEDIA_URL'):
        settings.CMS_PLUGIN_PHLOG_MEDIA_URL = settings.MEDIA_URL + 'cmsplugin_phlog/'
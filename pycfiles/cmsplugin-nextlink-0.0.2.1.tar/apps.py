# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/apps.py
# Compiled at: 2016-06-07 17:28:14
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CMSPluginNewsPlusConfig(AppConfig):
    name = 'cmsplugin_newsplus'
    verbose_name = _('News App')
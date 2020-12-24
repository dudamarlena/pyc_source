# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/apps.py
# Compiled at: 2016-06-07 17:28:14
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CMSPluginNewsPlusConfig(AppConfig):
    name = 'cmsplugin_newsplus'
    verbose_name = _('News App')
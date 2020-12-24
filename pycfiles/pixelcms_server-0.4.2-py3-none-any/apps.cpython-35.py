# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/settings/apps.py
# Compiled at: 2016-08-17 13:35:05
# Size of source mod 2**32: 184 bytes
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SettingsConfig(AppConfig):
    name = 'cms.settings'
    verbose_name = _('Settings')
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cmsplugin_twitter/models.py
# Compiled at: 2019-07-23 02:11:51
# Size of source mod 2**32: 858 bytes
from __future__ import absolute_import
from django.db import models
import django.utils.translation as _
from cms.models.pluginmodel import CMSPlugin

class Twitter(CMSPlugin):
    THEME_CHOICES = (
     (
      'light', _('Light')),
     (
      'dark', _('Dark')))
    username = models.CharField((_('Twitter handle')), max_length=75)
    widget_id = models.CharField((_('Widget id')), max_length=100, help_text=(_('Create a widget at <a href="https://twitter.com/settings/widgets" target="_blank">https://twitter.com/settings/widgets</a> and copy/paste the id of the widget into this field.')))
    theme = models.CharField((_('Theme')), max_length=5, choices=THEME_CHOICES)
    width = models.CharField((_('Width in pixels')), max_length=4)
    height = models.CharField((_('Height in pixels')), max_length=4)
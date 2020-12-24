# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/contrib/staging/apps.py
# Compiled at: 2015-11-11 23:34:03
from django.apps.config import AppConfig

class StagingConfig(AppConfig):
    name = 'ginger.contrib.staging'
    verbose_name = 'Staging'
    settings_module = 'ginger.contrib.staging.settings'
    settings_key = 'STAGING'
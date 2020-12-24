# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kubus/workspace/django-dbtemplate/dbtemplate/apps.py
# Compiled at: 2015-06-08 01:34:17
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DBTemplateConfig(AppConfig):
    name = 'dbtemplate'
    verbose_name = _('Templates')
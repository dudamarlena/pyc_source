# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-country-dialcode/country_dialcode/apps.py
# Compiled at: 2015-05-22 10:33:08
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CountryDialcodeConfig(AppConfig):
    name = 'country_dialcode'
    verbose_name = _('Country Dialcode')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/syndication/apps.py
# Compiled at: 2019-02-14 00:35:17
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SyndicationConfig(AppConfig):
    name = 'django.contrib.syndication'
    verbose_name = _('Syndication')
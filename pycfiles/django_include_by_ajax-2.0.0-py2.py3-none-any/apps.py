# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/archatas/Projects/django_include_by_ajax/project/django_include_by_ajax/include_by_ajax/apps.py
# Compiled at: 2018-10-27 21:08:59
from __future__ import unicode_literals
import re
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class IncludeByAjaxConfig(AppConfig):
    name = b'include_by_ajax'
    verbose_name = _(b'Include by Ajax')
    WEB_CRAWLERS = getattr(settings, b'INCLUDE_BY_AJAX_WEB_CRAWLERS', ('Googlebot',
                                                                       'Bingbot',
                                                                       'Slurp', 'DuckDuckBot',
                                                                       'Baiduspider',
                                                                       'YandexBot',
                                                                       'Sogou', 'Exabot',
                                                                       'ia_archiver'))
    web_crawler_pattern = re.compile((b'|').join(sorted(WEB_CRAWLERS, reverse=True)), flags=re.IGNORECASE)

    def ready(self):
        pass
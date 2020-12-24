# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/stats/cms_apps.py
# Compiled at: 2018-03-26 19:55:31
# Size of source mod 2**32: 413 bytes
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class StatsApphook(CMSApp):
    name = _('Stats Apphook')

    def get_urls(self, page=None, language=None, **kwargs):
        return ['danceschool.stats.urls']


apphook_pool.register(StatsApphook)
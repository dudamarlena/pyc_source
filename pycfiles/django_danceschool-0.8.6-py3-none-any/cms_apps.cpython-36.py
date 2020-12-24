# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/stats/cms_apps.py
# Compiled at: 2019-04-03 22:56:32
# Size of source mod 2**32: 413 bytes
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class StatsApphook(CMSApp):
    name = _('Stats Apphook')

    def get_urls(self, page=None, language=None, **kwargs):
        return [
         'danceschool.stats.urls']


apphook_pool.register(StatsApphook)
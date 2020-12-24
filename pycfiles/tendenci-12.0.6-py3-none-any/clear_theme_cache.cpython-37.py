# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme/management/commands/clear_theme_cache.py
# Compiled at: 2020-02-26 14:49:28
# Size of source mod 2**32: 903 bytes
from django.core.management.base import BaseCommand
from django.conf import settings
import django.core.cache as cache

class Command(BaseCommand):
    __doc__ = '\n    If theme files are served on an external server, such as AWS S3,\n    the theme files contents are cached and the cache keys are added\n    to a list that is also cached. This command clears that list, so\n    that theme files are then re-cached.\n\n    A usecase for this would be whenever a new theme is uploaded to the remote storage.\n\n    Usage: manage.py clear_theme_cache\n    '

    def handle(self, *args, **options):
        cache_group_key = '%s.theme_files_cache_list' % settings.SITE_CACHE_KEY
        cache_group_list = cache.get(cache_group_key)
        if cache_group_list:
            for key in cache_group_list:
                cache.delete(key)

            cache.set(cache_group_key, [])
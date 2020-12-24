# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/management/commands/clear_cache.py
# Compiled at: 2020-02-26 14:49:27
# Size of source mod 2**32: 229 bytes
from django.core.management.base import BaseCommand
import django.core.cache as cache

class Command(BaseCommand):
    __doc__ = '\n    Clears the entire site cache\n    '

    def handle(self, *args, **options):
        cache.clear()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/uvena_de/django_clear_memcache/management/commands/clear_memcache.py
# Compiled at: 2017-04-17 10:28:17
# Size of source mod 2**32: 686 bytes
from django_clear_memcache.clear import ClearMemcacheController
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clear all keys from the configured default memcache server using the configured prefix'
    can_import_settings = True

    def handle(self, **options):
        verbosity = int(options.get('verbosity', 0))
        controller = ClearMemcacheController()
        result = controller.clear_cache()
        if verbosity >= 1:
            return result
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/waitressd/management/commands/debugcache.py
# Compiled at: 2018-03-07 13:52:04
# Size of source mod 2**32: 453 bytes
import threading
from django.core.management.base import BaseCommand
from django.core.cache import caches

def get_from_cache(cache):
    cache.get('foo')


def func():
    cache = caches['default']
    for i in range(10):
        thread = threading.Thread(target=get_from_cache, args=(cache,))
        thread.start()
        thread.join()


class Command(BaseCommand):
    help = 'Debug cache'

    def handle(self, *args, **options):
        func()
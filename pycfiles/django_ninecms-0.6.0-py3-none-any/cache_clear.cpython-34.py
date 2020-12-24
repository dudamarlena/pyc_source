# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/rabelvideo/ninecms/management/commands/cache_clear.py
# Compiled at: 2015-11-05 11:14:05
# Size of source mod 2**32: 560 bytes
""" Management command for clearing cache """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.core.management import BaseCommand
from ninecms.utils.status import cache_clear

class Command(BaseCommand):
    help = 'Clears the cache.'

    def handle(self, *args, **options):
        """ Core function
        :param args: None
        :param options: None
        :return: None
        """
        cache_clear()
        self.stdout.write('Cache cleared.')
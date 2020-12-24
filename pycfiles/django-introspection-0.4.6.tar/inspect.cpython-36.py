# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo88/mogo/introspection/management/commands/inspect.py
# Compiled at: 2017-12-10 04:38:02
# Size of source mod 2**32: 479 bytes
from __future__ import print_function
from django.core.management.base import BaseCommand
from goerr import err
from introspection.inspector import inspect

class Command(BaseCommand):
    help = 'Inspect an application or model'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        inspect.scanapp(path)
        if err.exists:
            err.trace()
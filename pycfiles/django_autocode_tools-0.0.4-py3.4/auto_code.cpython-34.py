# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/management/commands/auto_code.py
# Compiled at: 2019-09-09 10:26:58
# Size of source mod 2**32: 927 bytes
from __future__ import print_function
from django.core.management.base import BaseCommand
from django_crontab.crontab import Crontab
from django_autocode_tools.auto_code import AutoCode

class Command(BaseCommand):
    help = '\n    add: automatically add restful api and basic orm operation.\n    remove: remove automatic add script.\n    refresh: refreshes serialized file'

    def add_arguments(self, parser):
        parser.add_argument('subcommand', choices=['add', 'remove', 'refresh'], help=self.help)
        parser.add_argument('jobhash', nargs='?')

    def handle(self, *args, **options):
        auto = AutoCode(**options)
        if options['subcommand'] == 'add':
            auto.add()
        else:
            if options['subcommand'] == 'remove':
                auto.remove()
            else:
                if options['subcommand'] == 'refresh':
                    auto.refresh()
                else:
                    print(self.help)
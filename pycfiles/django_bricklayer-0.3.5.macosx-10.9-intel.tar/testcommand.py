# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/bricklayer/management/commands/testcommand.py
# Compiled at: 2013-11-21 19:28:55
from django.core.management.base import BaseCommand
from bricklayer.utils import ColoredOutputMixin

class Command(ColoredOutputMixin, BaseCommand):
    help = 'Help text goes here'

    def handle(self, *args, **options):
        self.stdout.write('normal')
        self.print_error('error')
        self.print_success('success')
        self.print_warning('warning')
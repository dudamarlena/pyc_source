# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/management/commands/subcommands/gtest.py
# Compiled at: 2013-01-07 22:49:42
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<command>'
    help = 'Debugging for GoScale (DEV).'

    def handle(self, *args, **options):
        print args
        self.test()

    def test(self):
        print 'test'
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-chameleon/chameleon/management/commands/lessc.py
# Compiled at: 2012-12-30 05:40:48
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'This command compiles all LESS files to css in your project.'

    def handle_noargs(self, **options):
        print 'testing...'
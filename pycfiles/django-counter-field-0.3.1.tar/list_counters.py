# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kajic/projects/django-counter-field/django_counter_field/management/commands/list_counters.py
# Compiled at: 2013-12-26 09:09:07
from django.core.management.base import NoArgsCommand
from django_counter_field.counter import counters

class Command(NoArgsCommand):
    help = 'List all registered counters.'

    def handle(self, **kwargs):
        for i, counter_name in enumerate(counters.keys(), 1):
            print '%s. %s' % (i, counter_name)
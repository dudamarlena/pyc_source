# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kajic/projects/django-counter-field/django_counter_field/management/commands/rebuild_counter.py
# Compiled at: 2014-02-09 13:41:37
import sys
from django.core.management.base import BaseCommand
from django.db.models import Count
from django_counter_field.counter import counters

class Command(BaseCommand):
    args = '<counter_name>'
    help = '\n    Rebuild the specified counter. Use python manage.py list_counters\n    for a list of available counters.\n    '

    def handle(self, *args, **options):
        if len(args) != 1:
            sys.exit('Usage: python manage.py rebuild_counter <counter_name>')
        counter_name = args[0]
        if counter_name not in counters:
            sys.exit('%s is not a registered counter' % counter_name)
        counter = counters[counter_name]
        parent_id = 0
        count = 0
        for child in counter.child_model.objects.all().order_by(counter.foreign_field.name):
            current_parrent_id = counter.parent_id(child)
            if parent_id != current_parrent_id:
                if parent_id > 0:
                    counter.set_counter_field(parent_id, count)
                parent_id = current_parrent_id
                count = 0
            if counter.is_in_counter(child):
                count = count + 1

        if parent_id > 0:
            counter.set_counter_field(parent_id, count)
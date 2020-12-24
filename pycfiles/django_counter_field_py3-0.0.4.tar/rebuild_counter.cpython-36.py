# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danila/Work/tmp/django_counter_field_py3/django_counter_field_py3/management/commands/rebuild_counter.py
# Compiled at: 2018-01-17 11:16:50
# Size of source mod 2**32: 966 bytes
import sys
from django.core.management.base import BaseCommand
from django.db.models import Count
from django_counter_field_py3.counter import counters

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
        parent_field = counter.foreign_field.name
        for parent in counter.parent_model.objects.all():
            parent_id = parent.id
            count = (counter.child_model.objects.filter)(**{parent_field: parent_id}).count()
            counter.set_counter_field(parent_id, count)
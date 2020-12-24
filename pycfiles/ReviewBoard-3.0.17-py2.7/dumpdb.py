# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/management/commands/dumpdb.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core import serializers
from django.core.management.base import NoArgsCommand
from django.db.models import get_apps, get_models

class Command(NoArgsCommand):
    """Management command to dump data from the database."""
    help = b'Dump a common serialized version of the database to stdout.'

    def handle_noargs(self, **options):
        """Handle the command."""
        models = []
        for app in get_apps():
            models.extend(get_models(app))

        OBJECT_LIMIT = 150
        serializer = serializers.get_serializer(b'json')()
        totalobjs = 0
        for model in models:
            totalobjs += model.objects.count()

        prev_pct = -1
        i = 0
        self.stderr.write(b'Dump the database. This may take a while...\n')
        self.stdout.write(b'# dbdump v1 - %s objects' % totalobjs)
        for model in models:
            count = model.objects.count()
            j = 0
            while j < count:
                for obj in model.objects.all()[j:j + OBJECT_LIMIT].iterator():
                    value = serializer.serialize([obj])
                    if value != b'[]':
                        self.stdout.write(value[1:-1])
                    i += 1
                    pct = i * 100 / totalobjs
                    if pct != prev_pct:
                        self.stderr.write(b'  [%s%%]\r' % pct)
                        self.stderr.flush()
                        prev_pct = pct

                j += OBJECT_LIMIT

        self.stderr.write(b'\nDone.\n')
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/fixture_magic/management/commands/custom_dump.py
# Compiled at: 2018-10-19 13:50:29
# Size of source mod 2**32: 2624 bytes
from __future__ import print_function
import sys
try:
    import json
except ImportError:
    import django.utils as json

from django.core.management.base import BaseCommand
try:
    from django.db.models import loading
except ImportError:
    import django.apps as loading

from django.core.serializers import serialize
from django.conf import settings
from django.template import Variable, VariableDoesNotExist
from fixture_magic.utils import add_to_serialize_list, reorder_json, serialize_me, serialize_fully

class Command(BaseCommand):
    help = 'Dump multiple pre-defined sets of objects into a JSON fixture.'

    def add_arguments(self, parser):
        parser.add_argument('dump_name')
        parser.add_argument('pk', nargs='+')
        parser.add_argument('--natural', default=False, action='store_true', dest='natural', help='Use natural keys if they are available.')

    def handle(self, *args, **options):
        dump_name = options['dump_name']
        pks = options['pk']
        dump_settings = settings.CUSTOM_DUMPS[dump_name]
        app_label, model_name = dump_settings['primary'].split('.')
        include_primary = dump_settings.get('include_primary', False)
        dump_me = loading.get_model(app_label, model_name)
        objs = dump_me.objects.filter(pk__in=[int(i) for i in pks])
        for obj in objs.all():
            for dep in dump_settings['dependents']:
                try:
                    thing = Variable('thing.%s' % dep).resolve({'thing': obj})
                    if hasattr(thing, 'all'):
                        thing = thing.all()
                    add_to_serialize_list([thing])
                except VariableDoesNotExist:
                    sys.stderr.write('%s not found' % dep)

            if not include_primary:
                dump_settings['dependents'] or add_to_serialize_list([obj])

        serialize_fully()
        data = serialize('json', [o for o in serialize_me if o is not None], indent=4,
          use_natural_foreign_keys=(options.get('natural', False)),
          use_natural_primary_keys=(options.get('natural', False)))
        data = reorder_json((json.loads(data)),
          (dump_settings.get('order', [])),
          ordering_cond=(dump_settings.get('order_cond', {})))
        print(json.dumps(data, indent=4))
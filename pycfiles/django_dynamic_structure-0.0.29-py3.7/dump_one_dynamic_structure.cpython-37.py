# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/management/commands/dump_one_dynamic_structure.py
# Compiled at: 2019-10-27 02:46:00
# Size of source mod 2**32: 952 bytes
import json
from django.core.management.base import BaseCommand
from dyn_struct.datatools import structure_to_dict
from dyn_struct.db import models

class Command(BaseCommand):
    help = 'Dump dynamic structure'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--id', dest='id')
        parser.add_argument('-n', '--name', dest='name')

    def handle(self, *args, **options):
        if not options.get('id'):
            assert options.get('name')
        else:
            instance_id = options.get('id')
            name = options.get('name')
            if instance_id:
                structure = models.DynamicStructure.objects.get(id=instance_id)
            else:
                structure = models.DynamicStructure.objects.get(name=name)
        structures_data = structure_to_dict(structure)
        dumped_data = json.dumps(structures_data, indent=2, ensure_ascii=False)
        dumped_data = dumped_data.encode('utf-8').decode('utf-8')
        print(dumped_data)
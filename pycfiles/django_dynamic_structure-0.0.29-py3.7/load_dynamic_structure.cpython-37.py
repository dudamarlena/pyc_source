# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/management/commands/load_dynamic_structure.py
# Compiled at: 2019-10-27 02:46:00
# Size of source mod 2**32: 587 bytes
import json
from django.core.management.base import BaseCommand
from dyn_struct.datatools import structure_from_dict

class Command(BaseCommand):
    help = 'Load dynamic structure'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', dest='file', type=str, required=True)

    def handle(self, *args, **options):
        print('Load ... ')
        with open(options['file'], 'r') as (file):
            structs_data = json.loads(file.read())
        for struct_info in structs_data:
            structure_from_dict(struct_info)

        print('Success!')
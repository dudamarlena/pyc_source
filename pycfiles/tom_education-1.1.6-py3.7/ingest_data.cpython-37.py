# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/management/commands/ingest_data.py
# Compiled at: 2020-04-30 08:35:11
# Size of source mod 2**32: 1156 bytes
from django.core.management.base import BaseCommand
from tom_observations.models import ObservationRecord
from tom_targets.models import Target
from tom_dataproducts.models import DataProduct
from tom_observations.facility import get_service_class

class Command(BaseCommand):
    help = 'Downloads data for all completed observations'

    def add_arguments(self, parser):
        parser.add_argument('--target_id', help='Download data for a single target')

    def handle(self, *args, **options):
        if options['target_id']:
            try:
                target = Target.objects.get(pk=(options['target_id']))
                observation_records = ObservationRecord.objects.filter(target=target)
            except Target.DoesNotExist:
                raise Exception('Invalid target id provided')

        else:
            observation_records = ObservationRecord.objects.all()
        for record in observation_records:
            if record.terminal:
                record.save_data()
                self.stdout.write(f"Saved data for {record}")

        return 'Success!'
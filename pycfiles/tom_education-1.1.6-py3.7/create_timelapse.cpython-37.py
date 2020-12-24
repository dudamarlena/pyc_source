# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/management/commands/create_timelapse.py
# Compiled at: 2019-10-03 10:38:20
# Size of source mod 2**32: 2031 bytes
import logging
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from tom_dataproducts.models import DataProductGroup
from tom_targets.models import Target
from tom_education.constants import RAW_FILE_EXTENSION
from tom_education.models import TimelapsePipeline, AsyncError
logging.getLogger('imageio').setLevel(logging.CRITICAL)

class Command(BaseCommand):
    help = 'Create a timelapse from a series of data products for a target'

    def add_arguments(self, parser):
        parser.add_argument('target_pk', type=int)

    def handle(self, *args, **options):
        target_pk = options['target_pk']
        try:
            target = Target.objects.get(pk=target_pk)
        except Target.DoesNotExist:
            raise CommandError("Target '{}' does not exist".format(target_pk))

        group_name = settings.TOM_EDUCATION_TIMELAPSE_GROUP_NAME
        try:
            group, _ = DataProductGroup.objects.get_or_create(name=group_name)
        except DataProductGroup.MultipleObjectsReturned:
            raise CommandError("Multiple data products groups found with name '{}'".format(group_name))

        prods = group.dataproduct_set.filter(target=target).exclude(data__endswith=RAW_FILE_EXTENSION)
        self.stdout.write("Creating timelapse of {n} files for target '{name}'...".format(n=(prods.count()),
          name=(target.name)))
        if not prods.exists():
            self.stdout.write('Nothing to do')
            return
        pipe = TimelapsePipeline.create_timestamped(target, prods)
        try:
            pipe.run()
        except AsyncError as ex:
            try:
                self.stderr.write(f"Failed to create timelapse: {ex}")
            finally:
                ex = None
                del ex

        else:
            prod = pipe.group.dataproduct_set.first()
            msg = f"Created timelapse {prod.data.file}"
            self.stdout.write(self.style.SUCCESS(msg))
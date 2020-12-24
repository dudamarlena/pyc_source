# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/management/commands/process_observation_alerts.py
# Compiled at: 2020-01-06 09:07:21
# Size of source mod 2**32: 3347 bytes
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from tom_dataproducts.models import DataProduct
from tom_observations.facility import get_service_class
from tom_education.constants import RAW_FILE_EXTENSION
from tom_education.models import ObservationAlert, TimelapsePipeline

class Command(BaseCommand):
    help = 'Update the status of observations with alerts, download any new data, create timelapses, and send notification emails.'
    IMAGE_FILE_SUFFIX = '.fits.fz'

    def handle(self, *args, **options):
        try:
            from_addr = settings.TOM_EDUCATION_FROM_EMAIL_ADDRESS
        except AttributeError:
            self.stderr.write('TOM_EDUCATION_FROM_EMAIL_ADDRESS not set in settings.py')
            return
        else:
            new_data_targets = set([])
            new_data_alerts = set([])
            for alert in ObservationAlert.objects.all():
                ob = alert.observation
                facility_class = get_service_class(ob.facility)
                facility = facility_class()
                if ob.status not in facility.get_terminal_observing_states():
                    facility.update_observation_status(ob.observation_id)
                    self.stdout.write('Checking for new data for observation {}'.format(ob.observation_id))
                    if facility.save_data_products(ob):
                        new_data_targets.add(ob.target)
                        new_data_alerts.add(alert)

            for target in new_data_targets:
                prods = target.dataproduct_set.filter(data__endswith=(self.IMAGE_FILE_SUFFIX)).exclude(data__endswith=RAW_FILE_EXTENSION)
                if not prods.exists():
                    continue
                new_pipeline = TimelapsePipeline.create_timestamped(target, prods)
                self.stdout.write('Creating timelapse for target {}'.format(target.name))
                try:
                    new_pipeline.run()
                except AsyncError as ex:
                    try:
                        self.stderr.write(f"Failed to create timelapse: {ex}")
                        return
                    finally:
                        ex = None
                        del ex

                new_tl = new_pipeline.group.dataproduct_set.first()
                timelapses = DataProduct.objects.filter(target=target,
                  data_product_type=(settings.DATA_PRODUCT_TYPES['timelapse'][0])).exclude(pk=(new_tl.pk)).all()
                for tl in timelapses:
                    tl.delete()
                    tl.data.delete(save=False)

            for alert in new_data_alerts:
                target = alert.observation.target
                subject = "Observation for '{}' has new data".format(target.name)
                message = "Your observation for '{}' has completed, and a timelapse is available".format(target.name)
                to = [alert.email]
                send_mail(subject, message, from_addr, to)

            self.stdout.write('Send {} email updates'.format(len(new_data_alerts)))
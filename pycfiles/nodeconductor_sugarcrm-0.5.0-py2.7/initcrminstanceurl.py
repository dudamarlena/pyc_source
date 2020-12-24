# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/management/commands/initcrminstanceurl.py
# Compiled at: 2016-09-28 11:51:43
from django.core.management.base import BaseCommand
from ...models import CRM

class Command(BaseCommand):
    help_text = 'Initialize CRMs instance_url field.'

    def handle(self, *args, **options):
        for crm in CRM.objects.all():
            try:
                b = crm.get_backend()
                crm.instance_url = b.get_crm_template_group_result_details(crm)['provisioned_resources']['OpenStack.Instance']
                crm.save()
            except Exception as e:
                self.stdout.write('Cannot initialize isntance_url for CRM: %s (UUID: %s). Error: %s' % (
                 crm.name, crm.uuid.hex, e))
            else:
                self.stdout.write('Successfully initialized instance url for CRM: %s (UUID: %s).' % (
                 crm.name, crm.uuid.hex))
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/management/commands/remove_tasks_for_disabled_parents.py
# Compiled at: 2018-02-23 09:57:43
# Size of source mod 2**32: 1530 bytes
from django.core.management.base import BaseCommand
from transmanager.models import TransModelLanguage
from transmanager.settings import TM_DEFAULT_ENABLED_ATTRIBUTE_NAME
from transmanager.tasks.tasks import delete_translations_for_item_and_its_children
from transmanager.utils import has_field

class Command(BaseCommand):
    help = 'Removes the tasks belonging to a deactivated parents.'

    def handle(self, *args, **options):
        filter_by = {TM_DEFAULT_ENABLED_ATTRIBUTE_NAME: False}
        whole_ids = []
        self.stdout.write('Start')
        for model in TransModelLanguage.objects.all():
            mc = model.get_model_class()
            if not has_field(mc, TM_DEFAULT_ENABLED_ATTRIBUTE_NAME):
                pass
            else:
                if mc.__name__ != 'Rental':
                    pass
                else:
                    disabled_ids = list(mc.objects.filter(**filter_by).values_list('id', flat=True))
                    whole_ids += disabled_ids
                    self.stdout.write('Model: {} has {} ids'.format(mc.__name__, len(disabled_ids)))
                    if disabled_ids:
                        for item_id in disabled_ids:
                            delete_translations_for_item_and_its_children.delay(mc, item_id)

        self.stdout.write('{} ids will be processed'.format(len(whole_ids)))
        self.stdout.write('End')
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/mixins.py
# Compiled at: 2017-07-27 05:10:22
# Size of source mod 2**32: 1741 bytes
import logging
from .settings import TM_DISABLED
from .tasks.tasks import create_translations_for_item_and_its_children, delete_translations_for_item_and_its_children
logger = logging.getLogger(__name__)

class TranslationTasksMixin(object):
    __doc__ = '\n    Mixin that allows to create/delete the translations tasks when the instance of the model is enabled/disabled\n    '

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        create = False
        delete = False
        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
        else:
            prev = None
        if not self.pk and self.enabled:
            create = True
        else:
            if self.pk and self.enabled and prev and not prev.enabled:
                create = True
            elif self.pk and not self.enabled and prev and prev.enabled:
                delete = True
        super().save(force_insert, force_update, using, update_fields)
        if not TM_DISABLED:
            if create:
                logger.info('XXXXXXXXXXXXXXXXXXXX')
                logger.info('CREATING FOR ITEM AND CHILDREN')
                create_translations_for_item_and_its_children.delay(self.__class__, self.pk)
                logger.info('END FOR ITEM AND CHILDREN\n\n')
        elif delete:
            logger.info('XXXXXXXXXXXXXXXXXXXX')
            logger.info('DELETING FOR ITEM AND CHILDREN')
            delete_translations_for_item_and_its_children.delay(self.__class__, self.pk)
            logger.info('END FOR ITEM AND CHILDREN\n\n')
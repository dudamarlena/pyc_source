# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/management/commands/unpublish.py
# Compiled at: 2015-09-16 10:11:00
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Q
from djinn_contenttypes.models.publishable import PublishableContent
from djinn_contenttypes.registry import CTRegistry
from django.utils import translation

class Command(BaseCommand):
    help = 'Publish contenttypes if need be'

    def handle(self, *args, **options):
        """Check contentitems that are beyond the publish_to date.  We just
        call 'save' on the instance, and let the signal handlers take
        care of the rest.

        """
        now = datetime.now()
        translation.activate('nl_NL')
        for ctype in CTRegistry.list_types():
            model = CTRegistry.get_attr(ctype, 'class')
            if issubclass(model, PublishableContent):
                for instance in model.objects.filter(unpublish_notified=False, publish_to__isnull=False).filter(Q(publish_to__lt=now) | Q(publish_from__gt=now)):
                    instance.unpublish_notified = True
                    instance.publish_notified = False
                    instance.save()

                for instance in model.objects.filter(remove_after_publish_to=True, publish_to__isnull=False, publish_to__lt=now):
                    instance.delete()
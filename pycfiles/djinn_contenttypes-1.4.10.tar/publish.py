# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/management/commands/publish.py
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
        """Check contentitems that just have reached published state
        due to publish timestamp. We just call 'save' on the instance,
        and let the signal handlers take care of the rest. """
        now = datetime.now()
        translation.activate('nl_NL')
        for ctype in CTRegistry.list_types():
            model = CTRegistry.get_attr(ctype, 'class')
            if issubclass(model, PublishableContent):
                for instance in model.objects.filter(publish_notified=False, publish_from__lt=now).filter(Q(publish_to__isnull=True) | Q(publish_to__gt=now)):
                    instance.save()
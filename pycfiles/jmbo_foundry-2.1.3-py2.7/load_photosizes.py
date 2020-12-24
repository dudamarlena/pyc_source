# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/jmbo-foundry/foundry/management/commands/load_photosizes.py
# Compiled at: 2015-01-27 08:59:34
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.importlib import import_module
from django.utils import simplejson
from django.core import serializers
from django.conf import settings
from photologue.models import PhotoSize

class Command(BaseCommand):
    help = 'Scan apps for fixtures/photosizes.json and loads them.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        for app in reversed(settings.INSTALLED_APPS):
            mod = import_module(app)
            fixtures = os.path.join(os.path.dirname(mod.__file__), 'fixtures', 'photosizes.json')
            if os.path.exists(fixtures):
                fp = open(fixtures, 'r')
                json = fp.read()
                fp.close()
                for obj in serializers.deserialize('json', json):
                    obj.object.id = None
                    try:
                        photosize = PhotoSize.objects.get(name=obj.object.name)
                    except PhotoSize.DoesNotExist:
                        pass
                    else:
                        obj.object.id = photosize.id

                    obj.save()

        return
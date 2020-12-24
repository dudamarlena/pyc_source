# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Nomensa/django-scrub-pii/scrubpii/management/commands/get_sensitive_data_removal_script.py
# Compiled at: 2016-01-29 10:01:28
# Size of source mod 2**32: 561 bytes
try:
    from django.apps import apps
except ImportError:
    from django.db import models as apps

from django.core.management.base import BaseCommand, CommandError
from scrubpii.utils import get_updates_for_model

class Command(BaseCommand):
    can_import_settings = True
    output_transaction = True

    def handle(self, *args, **options):
        models = apps.get_models()
        script = ''
        for model in models:
            updates = get_updates_for_model(model)
            if updates:
                script += updates
                continue

        return script
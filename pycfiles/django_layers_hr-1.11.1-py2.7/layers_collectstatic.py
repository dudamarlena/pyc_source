# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/management/commands/layers_collectstatic.py
# Compiled at: 2018-03-27 03:51:51
import os
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import management
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.functional import empty
from layers import get_layer_stacks

class Command(BaseCommand):
    help = 'Run collectstatic for each layer. You must use the new style LAYERS format for this to work.'

    @transaction.atomic
    def handle(self, *args, **options):
        original_static_root = settings.STATIC_ROOT
        for layer in get_layer_stacks().keys():
            settings.LAYERS['current'] = layer
            settings.STATIC_ROOT = os.path.join(original_static_root, layer)
            default_storage._wrapped = empty
            staticfiles_storage._wrapped = empty
            management.call_command('collectstatic', interactive=False)
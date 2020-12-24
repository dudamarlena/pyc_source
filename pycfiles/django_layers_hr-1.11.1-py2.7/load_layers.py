# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/management/commands/load_layers.py
# Compiled at: 2018-03-27 03:51:51
from django.core.management.base import BaseCommand
from django.db import transaction
from layers import get_layer_stacks, reset_layer_stacks, build_layer_stacks
from layers.models import Layer

class Command(BaseCommand):
    help = 'Create objects from layers setting.'

    @transaction.atomic
    def handle(self, *args, **options):
        reset_layer_stacks()
        build_layer_stacks()
        for layers in get_layer_stacks().values():
            for layer in layers:
                Layer.objects.get_or_create(name=layer)
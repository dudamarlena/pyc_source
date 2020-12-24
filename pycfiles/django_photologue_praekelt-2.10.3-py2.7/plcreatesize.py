# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/photologue/management/commands/plcreatesize.py
# Compiled at: 2014-04-07 04:12:05
from django.core.management.base import BaseCommand, CommandError
from photologue.management.commands import create_photosize

class Command(BaseCommand):
    help = 'Creates a new Photologue photo size interactively.'
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        create_size(args[0])


def create_size(size):
    create_photosize(size)
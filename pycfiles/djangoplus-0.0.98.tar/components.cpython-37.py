# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/ui/management/commands/components.py
# Compiled at: 2019-04-02 19:15:35
# Size of source mod 2**32: 484 bytes
from djangoplus.tools import terminal
from djangoplus.ui.components import Component
from django.core.management.base import BaseCommand
from djangoplus.docs.utils import extract_documentation

class Command(BaseCommand):

    def handle(self, *args, **options):
        for cls in Component.subclasses():
            name = terminal.bold(cls.__name__)
            description = extract_documentation(cls)
            print('{}: {}'.format(name, description))
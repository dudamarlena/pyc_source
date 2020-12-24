# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/exportme/core/management/commands/list.py
# Compiled at: 2018-11-12 07:24:41
# Size of source mod 2**32: 1230 bytes
from prometheus_client import CollectorRegistry, generate_latest
from exportme.core.models import EXPORTERS, ApiKey
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('collector', nargs='?')
        parser.add_argument('username', nargs='?')

    @property
    def apikey(self):
        return get_object_or_404(ApiKey,
          owner__username=(self.username), service=(self.entry.module_name)).key

    def get(self, entry):
        try:
            self.entry = entry
            self.module = entry.load()
        except ImportError as e:
            try:
                print('Error loading')
            finally:
                e = None
                del e

        else:
            registry = CollectorRegistry()
            registry.register(self.module(self))
            print(generate_latest(registry).decode('utf8'))

    def handle(self, collector, username, **options):
        if collector is None:
            for entry in EXPORTERS:
                print(entry)

        else:
            for entry in EXPORTERS:
                if collector == entry.name:
                    self.username = username
                    return self.get(entry)
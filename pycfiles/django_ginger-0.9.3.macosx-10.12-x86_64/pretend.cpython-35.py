# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/pretend.py
# Compiled at: 2015-05-20 12:25:22
# Size of source mod 2**32: 1384 bytes
import pprint
from optparse import make_option
from django.apps import apps
from django.db import models
from ginger import pretenses
from django.core.management import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'app_name.model_name'
    help = 'Create data for the specified model'

    def add_arguments(self, parser):
        parser.add_argument('model')
        parser.add_argument('-t', '--total', default=20, type=int, help='Total number of instances to be created')
        parser.add_argument('-p', '--pretense', default=None, help='Pretense to be used for content generation')

    def handle(self, **options):
        name = options['model']
        if '.' in name:
            app_label, model_name = name.split('.', 1)
            model = apps.get_model(app_label, model_name)
        else:
            try:
                model = next(m for m in apps.get_models() if m.__name__.lower() == name.lower())
            except StopIteration:
                raise ValueError('No model found: %r' % name)

        pretense = options['pretense']
        verbose = int(options['verbosity']) > 1
        callback = self.verbose if verbose else None
        pretenses.generate(model, options['total'], name=pretense, callback=callback)

    def verbose(self, data):
        self.stdout.write(pprint.pformat(data, indent=4))
        self.stdout.write('\n')
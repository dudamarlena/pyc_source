# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/create_model_views.py
# Compiled at: 2015-01-03 12:40:26
import optparse
from django.core.management import BaseCommand
from django.core.management.base import CommandError
from ginger.generators import views

class Command(BaseCommand):
    view_types = [
     'new', 'detail', 'edit', 'search', 'list', 'form', 'form-done', 'wizard']
    help = 'Create views associated with a model for the provided types'
    args = 'app_name.ResourceName type [type ..]'
    option_list = BaseCommand.option_list + (
     optparse.make_option('-m', '--model', action='store', help='Model associated with the view.\nThis maybe needed when resource name is different from model name'),)

    def handle(self, *args, **options):
        args = list(args)
        if len(args) < 2:
            raise CommandError('No app_name.ResourceName type [type ...] has been provided. \n\n%s' % self.usage(''))
        view = args.pop(0)
        app_name, resource = view.split('.', 1)
        resource = '%sObject' % (resource,)
        app = views.Application(app_name, resource, options['model'])
        kinds = list(args)
        kinds = tuple(filter(lambda a: bool(a), (k.strip(', ') for k in kinds if k)))
        app.generate_model_views(kinds)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/patch_view.py
# Compiled at: 2015-05-20 12:22:35
import optparse, inspect, importlib
from django.core.management import BaseCommand
from django.core.management.base import CommandError
from django.utils.module_loading import import_string
from ginger.views import GingerView, utils
from ginger.meta import views

class Command(BaseCommand):
    view_types = [
     'new', 'detail', 'edit', 'search', 'list', 'form', 'form-done', 'wizard', 'template']
    help = 'Creates a view and its associated forms/templates. If any class already exists then it will never be over-written.'

    def add_arguments(self, parser):
        parser.add_argument('view')

    def handle(self, **options):
        view = options['view']
        try:
            view_class = importlib.import_module(view)
        except ImportError:
            view_class = import_string(view)

        if inspect.ismodule(view_class):
            view_classes = utils.find_views(view_class)
        else:
            view_classes = [
             view_class]
        for view in view_classes:
            app = views.ViewPatch(view)
            app.patch()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shaun/Projects/tv-app/ve/src/django-generate/generate/management/commands/generate.py
# Compiled at: 2012-09-18 09:25:04
import time, imp
from django.core.management.base import BaseCommand
from json_loader import load_json

class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        from django.db.models import get_app, get_apps
        exclude = options.get('exclude', [])
        excluded_apps = [ get_app(app_label) for app_label in exclude ]
        if len(app_labels) == 0:
            app_list = [ app for app in get_apps() if app not in excluded_apps ]
        else:
            app_list = [ get_app(app_label) for app_label in app_labels ]
        for app in app_list:
            name = app.__name__.replace('.models', '')
            app_path = __import__(name, {}, {}, [name.split('.')[(-1)]]).__path__
            try:
                params = imp.find_module('generator', app_path)
            except ImportError:
                pass
            else:
                generator = imp.load_module((name + '.generator'), *params)
                print 'Generating items for %s.' % name.title()
                start = time.time()
                load_json(generator.generate())
                now = time.time()
                print 'Generation completed in %s seconds' % (now - start)
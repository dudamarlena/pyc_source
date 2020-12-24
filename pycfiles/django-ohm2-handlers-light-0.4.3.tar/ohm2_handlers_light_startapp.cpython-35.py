# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_handlers_light/management/commands/ohm2_handlers_light_startapp.py
# Compiled at: 2017-09-22 11:48:26
# Size of source mod 2**32: 3142 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from subprocess import call
import os, shutil

def load_template(template, name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), template)
    with open(path, 'r') as (f):
        content = f.read()
    return content.format(name.upper(), name.lower(), name.title(), h_utils.get_random_string(32), int(h_utils.random_string_hexdigits(3), 16) * 64)


def append(filename, text):
    with open(filename, 'a') as (f):
        f.write(text)


def override(filename, text):
    with open(filename, 'w') as (f):
        f.write(text)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-a', '--app')
        parser.add_argument('-m', '--move')

    def handle(self, *args, **options):
        app = options['app']
        move = options.get('move')
        if move:
            move_to = os.path.join(move, app)
            exist = os.path.isdir(move_to)
            if exist:
                self.stdout.write('Final destination already exist')
                return
        else:
            move_to = None
        call('./manage.py startapp ' + app, shell=True)
        os.makedirs(app + '/management')
        override(app + '/management/__init__.py', '')
        os.makedirs(app + '/management/commands')
        override(app + '/management/commands/__init__.py', '')
        os.makedirs(app + '/static')
        os.makedirs(app + '/static/' + app)
        os.makedirs(app + '/templates')
        os.makedirs(app + '/templates/' + app)
        to_run = [
         {'src': 'templates/app_test_command.template', 'dst': app + '/management/commands/' + app + '_test_command.py', 'func': override},
         {'src': 'templates/app_settings.template', 'dst': app + '/settings.py', 'func': override},
         {'src': 'templates/app_definitions.template', 'dst': app + '/definitions.py', 'func': override},
         {'src': 'templates/app_errors.template', 'dst': app + '/errors.py', 'func': override},
         {'src': 'templates/app_decorators.template', 'dst': app + '/decorators.py', 'func': override},
         {'src': 'templates/app_utils.template', 'dst': app + '/utils.py', 'func': override},
         {'src': 'templates/app_models.template', 'dst': app + '/models.py', 'func': override},
         {'src': 'templates/app_managers.template', 'dst': app + '/managers.py', 'func': override},
         {'src': 'templates/app_urls.template', 'dst': app + '/urls.py', 'func': override},
         {'src': 'templates/app_views.template', 'dst': app + '/views.py', 'func': override},
         {'src': 'templates/app_dispatcher.template', 'dst': app + '/dispatcher.py', 'func': override},
         {'src': 'templates/app_middlewares.template', 'dst': app + '/middlewares.py', 'func': override},
         {'src': 'templates/app_admin.template', 'dst': app + '/admin.py', 'func': override},
         {'src': 'templates/app_serializers.template', 'dst': app + '/serializers.py', 'func': override},
         {'src': 'templates/app_context_processors.template', 'dst': app + '/context_processors.py', 'func': override}]
        for run in to_run:
            text = load_template(run['src'], app)
            run['func'](run['dst'], text)

        if move_to:
            shutil.move(app, move_to)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/development/v0.4.0/website/handlers/management/commands/handlers_create_api.py
# Compiled at: 2016-05-31 22:54:20
# Size of source mod 2**32: 3552 bytes
from django.core.management.base import BaseCommand, CommandError
from handlers import utils as h_utils
from subprocess import call
import os

def load_template(template, name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), template)
    with open(path, 'r') as (f):
        content = f.read()
    return content.format(name.upper(), name.lower(), name.title(), h_utils.get_random_string(32), int(h_utils.random_string_hexdigits(3), 16) * 64)


def write(filename, text):
    with open(filename, 'a') as (f):
        f.write(text)


def override(filename, text):
    with open(filename, 'w') as (f):
        f.write(text)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        call('./manage.py startapp api', shell=True)
        app = 'api'
        os.makedirs(app + '/management')
        override(app + '/management/__init__.py', '')
        os.makedirs(app + '/management/commands')
        override(app + '/management/commands/__init__.py', '')
        os.makedirs(app + '/static')
        os.makedirs(app + '/static/' + app)
        os.makedirs(app + '/static/' + app + '/android')
        os.makedirs(app + '/static/' + app + '/android/css')
        os.makedirs(app + '/static/' + app + '/android/images')
        os.makedirs(app + '/static/' + app + '/android/js')
        os.makedirs(app + '/static/' + app + '/android/other')
        os.makedirs(app + '/static/' + app + '/ios')
        os.makedirs(app + '/static/' + app + '/ios/css')
        os.makedirs(app + '/static/' + app + '/ios/images')
        os.makedirs(app + '/static/' + app + '/ios/js')
        os.makedirs(app + '/static/' + app + '/ios/other')
        os.makedirs(app + '/static/' + app + '/default')
        os.makedirs(app + '/static/' + app + '/default/css')
        os.makedirs(app + '/static/' + app + '/default/images')
        os.makedirs(app + '/static/' + app + '/default/js')
        os.makedirs(app + '/static/' + app + '/default/other')
        text = load_template('app_test_command.template', app)
        write(app + '/management/commands/' + app + '_test_command.py', text)
        text = load_template('app_settings.template', app)
        write(app + '/settings.py', text)
        text = load_template('app_definitions.template', app)
        write(app + '/definitions.py', text)
        text = load_template('api_errors.template', app)
        write(app + '/errors.py', text)
        text = load_template('app_decorators.template', app)
        write(app + '/decorators.py', text)
        text = load_template('app_utils.template', app)
        write(app + '/utils.py', text)
        text = load_template('app_models.template', app)
        override(app + '/models.py', text)
        text = load_template('app_urls.template', app)
        write(app + '/urls.py', text)
        text = load_template('app_views.template', app)
        override(app + '/views.py', text)
        text = load_template('api_apis.template', app)
        write(app + '/apis.py', text)
        text = load_template('app_viewsdispatcher.template', app)
        write(app + '/viewsdispatcher.py', text)
        text = load_template('api_apisdispatcher.template', app)
        write(app + '/apisdispatcher.py', text)
        text = load_template('app_middlewares.template', app)
        write(app + '/middlewares.py', text)
        text = load_template('app_admin.template', app)
        override(app + '/admin.py', text)
        text = load_template('app_crons.template', app)
        override(app + '/crons.py', text)
        text = load_template('app_managers.template', app)
        override(app + '/managers.py', text)
        text = load_template('app_tasks.template', app)
        write(app + '/tasks.py', text)
        text = load_template('app_serializers.template', app)
        write(app + '/serializers.py', text)
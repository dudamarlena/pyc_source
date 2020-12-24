# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/development/002/website/apps/ohm2_handlers/management/commands/handlers_startapp.py
# Compiled at: 2016-06-17 16:30:52
# Size of source mod 2**32: 6340 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers import utils as h_utils
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
        parser.add_argument('-a', '--app')

    def handle(self, *args, **options):
        app = options['app']
        call('./manage.py startapp ' + app, shell=True)
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
        os.makedirs(app + '/templates')
        os.makedirs(app + '/templates/' + app)
        os.makedirs(app + '/templates/' + app + '/android')
        os.makedirs(app + '/templates/' + app + '/ios')
        os.makedirs(app + '/templates/' + app + '/default')
        text = load_template('app_test_command.template', app)
        write(app + '/management/commands/' + app + '_test_command.py', text)
        text = load_template('app_settings.template', app)
        write(app + '/settings.py', text)
        text = load_template('app_definitions.template', app)
        write(app + '/definitions.py', text)
        text = load_template('app_errors.template', app)
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
        text = load_template('app_apis.template', app)
        write(app + '/apis.py', text)
        text = load_template('app_viewsdispatcher.template', app)
        write(app + '/viewsdispatcher.py', text)
        text = load_template('app_apisdispatcher.template', app)
        write(app + '/apisdispatcher.py', text)
        text = load_template('app_middlewares.template', app)
        write(app + '/middlewares.py', text)
        text = load_template('app_admin.template', app)
        override(app + '/admin.py', text)
        text = load_template('app_crons.template', app)
        override(app + '/crons.py', text)
        text = load_template('app_base_template.template', app)
        write(app + '/templates/' + app + '/base_template.html', text)
        text = load_template('app_managers.template', app)
        override(app + '/managers.py', text)
        text = load_template('app_tasks.template', app)
        write(app + '/tasks.py', text)
        text = load_template('app_template_android_links.template', app)
        write(app + '/templates/' + app + '/android/links.html', text)
        text = load_template('app_template_android_scripts.template', app)
        write(app + '/templates/' + app + '/android/scripts.html', text)
        text = load_template('app_template_android_body.template', app)
        write(app + '/templates/' + app + '/android/body.html', text)
        text = load_template('app_template_android_index.template', app)
        write(app + '/templates/' + app + '/android/index.html', text)
        text = load_template('app_template_android_js_index.template', app)
        write(app + '/static/' + app + '/android/js/index.js', text)
        text = load_template('app_template_android_css_index.template', app)
        write(app + '/static/' + app + '/android/css/index.css', text)
        text = load_template('app_template_ios_links.template', app)
        write(app + '/templates/' + app + '/ios/links.html', text)
        text = load_template('app_template_ios_scripts.template', app)
        write(app + '/templates/' + app + '/ios/scripts.html', text)
        text = load_template('app_template_ios_body.template', app)
        write(app + '/templates/' + app + '/ios/body.html', text)
        text = load_template('app_template_ios_index.template', app)
        write(app + '/templates/' + app + '/ios/index.html', text)
        text = load_template('app_template_ios_js_index.template', app)
        write(app + '/static/' + app + '/ios/js/index.js', text)
        text = load_template('app_template_ios_css_index.template', app)
        write(app + '/static/' + app + '/ios/css/index.css', text)
        text = load_template('app_template_default_links.template', app)
        write(app + '/templates/' + app + '/default/links.html', text)
        text = load_template('app_template_default_scripts.template', app)
        write(app + '/templates/' + app + '/default/scripts.html', text)
        text = load_template('app_template_default_body.template', app)
        write(app + '/templates/' + app + '/default/body.html', text)
        text = load_template('app_template_default_index.template', app)
        write(app + '/templates/' + app + '/default/index.html', text)
        text = load_template('app_template_default_js_index.template', app)
        write(app + '/static/' + app + '/default/js/index.js', text)
        text = load_template('app_template_default_css_index.template', app)
        write(app + '/static/' + app + '/default/css/index.css', text)
        text = load_template('app_serializers.template', app)
        write(app + '/serializers.py', text)
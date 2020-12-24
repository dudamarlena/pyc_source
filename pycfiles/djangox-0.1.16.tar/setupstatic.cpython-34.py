# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/youngrok/workspace/djangox/djangox/apps/tools/management/commands/setupstatic.py
# Compiled at: 2015-10-20 05:43:18
# Size of source mod 2**32: 1076 bytes
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from mako.template import Template
from djangox.apps import import_app, tools

class Command(BaseCommand):
    args = 'app name'
    help = 'Setup static folder for specified app.\n - create static folder\n - ready to use bower\n   - generate .bowerrc and bower.json\n   - bower packages will be installed in static/lib\n   - bootstrap, font-awesome, jquery will be included in bower.json by default.\n'

    def handle(self, *args, **options):
        app_name = args[0]
        os.makedirs(app_name + '/' + 'static/lib', exist_ok=True)
        template_path = filename = tools.__path__[0] + '/setupstatic/'
        with open(app_name + '/../.bowerrc', 'w') as (f):
            f.write(Template(filename=template_path + '.bowerrc').render(app_name=app_name))
        with open(app_name + '/../bower.json', 'w') as (f):
            f.write(Template(filename=template_path + 'bower.json').render(app_name=app_name))
        print('Now you can use bower command. Try `bower install`.')
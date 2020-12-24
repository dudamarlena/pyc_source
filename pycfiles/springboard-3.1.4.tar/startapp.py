# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/tools/commands/startapp.py
# Compiled at: 2015-11-17 11:55:31
import os, pkg_resources, shutil
from cookiecutter.main import cookiecutter
from springboard.tools.commands.base import SpringboardToolCommand, CommandArgument

class StartAppTool(SpringboardToolCommand):
    command_name = 'startapp'
    command_help_text = 'Create new applicaton scaffolding'
    command_arguments = (
     CommandArgument('app_name', metavar='app_name', help='The name of the application to start.'),
     CommandArgument('--security-key', dest='thumbor_security_key', default='', help='The thumbor security key to use.'),
     CommandArgument('-a', '--author', dest='author', default='', help="The author's name."),
     CommandArgument('-e', '--author-email', dest='author_email', default='', help="The author's email address."),
     CommandArgument('--url', dest='url', default='', help="The project's URL."),
     CommandArgument('-l', '--license', dest='license', default='BSD', help="The application's licence."),
     CommandArgument('-p', '--prompt', dest='no_input', default=True, action='store_false'))

    def run(self, **options):
        cookiecutter(pkg_resources.resource_filename('springboard', 'tools/commands/cookiecutter/startapp'), no_input=options.pop('no_input'), extra_context=options)
        asset_directories = [
         'templates', 'static']
        for asset_dir in asset_directories:
            shutil.copytree(pkg_resources.resource_filename('springboard', asset_dir), os.path.join(options['app_name'], options['app_name'], asset_dir))
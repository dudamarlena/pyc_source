# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo88/mogo/introspection/terminal/commands.py
# Compiled at: 2017-12-26 08:16:04
# Size of source mod 2**32: 1414 bytes
from goerr import err
from django.conf import settings
from introspection.inspector import inspect
from term.commands import Command, rprint
import json

def inspectapp(request, cmd_args):
    inspect.scanapp((cmd_args[0]), term=True)
    if err.exists:
        err.new('Error inspecting app', inspectapp)
        rprint('Error scanning app', err.to_json(indent=2))


def setting_apps():
    apps = inspect.appnames
    rprint('Found', len(apps), 'apps')
    for app in apps:
        rprint(app)


def setting(request, cmd_args):
    if len(cmd_args) == 0:
        return 'Not enough arguments: ex: setting apps'
    else:
        if cmd_args[0] == 'apps':
            return setting_apps()
        else:
            s = getattr(settings, cmd_args[0], None)
            if s is None:
                return 'Setting ' + cmd_args[0] + ' not found'
            msg = ''
            try:
                msg = json.dumps(s, indent=2).replace(' ', '&nbsp;').replace('\n', '<br />')
            except:
                msg = str(s)

        rprint(msg)
        return


c0 = Command('setting', setting, 'Show a setting: ex: setting apps')
c1 = Command('inspect', inspectapp, 'Inspect an app: ex: inspect auth')
COMMANDS = [
 c0, c1]
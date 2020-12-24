# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\delicious.py
# Compiled at: 2009-03-24 20:56:20
""" Backup for Delicious bookmarks
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: delicious.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $'
import sys, logging, os.path
from types import *
from optparse import OptionParser
levelsUp = 3
path = os.path.abspath(__file__)
while levelsUp > 0:
    path = os.path.dirname(path)
    levelsUp = levelsUp - 1

sys.path.append(path)
import jld.api as api, jld.registry as reg, jld.backup.delicious_messages as msg, jld.backup.delicious_ui as dui, jld.backup.delicious_defaults as ddef
from jld.backup.delicious_backup import Backup
from jld.tools.template import ExTemplate
import jld.tools.logger as dlogger
_options = [{'o1': '-u', 'var': 'username', 'action': 'store', 'help': 'config_username', 'reg': True, 'default': None}, {'o1': '-p', 'var': 'password', 'action': 'store', 'help': 'config_password', 'reg': True, 'default': None}, {'o1': '-f', 'var': 'db_path', 'action': 'store', 'help': 'config_db_file', 'reg': True, 'default': None}, {'o1': '-l', 'var': 'syslog', 'action': 'store_true', 'help': 'syslog', 'reg': False, 'default': False}]

def main():
    msgs = msg.Delicious_Messages()
    ui = dui.Delicious_UI()
    ui.setParams(msgs)
    try:
        backup = Backup()
        usage_template = "%prog [options] command\n    \nversion $Id: delicious.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $ by Jean-Lou Dupont\n\n*** Interface to Delicious (http://www.delicious.com/) ***\n\nUsage notes:\n  1- for high-rate updates, use the ''updatedb'' command\n  2- for low-rate updates, use the ''updatedbfull'' command.\n  The ''low-rate updates'' should be used no more than once per hour in order to respect the Delicious policy.\n  \n\nThe commands which generate log entries are flagged with (logged) below.\n\nCommands:\n^^{commands}"
        commands_help = backup.genCommandsHelp()
        tpl = ExTemplate(usage_template)
        usage = tpl.substitute({'commands': commands_help})
        ui.handleArguments(usage, _options)
        _syslog = False if ui.options.syslog else True
        logger = dlogger.logger('dlc', include_console=False, include_syslog=_syslog)
        backup.logger = logger
        ui.logger = logger
        r = reg.Registry('delicious')
        ui.updateRegistry(r, _options, ui.options)
        params = {}
        ui.integrateOptions(ui.options, params, _options)
        defs = ddef.Delicious_Defaults()
        ui.integrateDefaults(defs, r, _options, params)
        ui.verifyType(params, _options)
        ui.copyOptions(params, backup, _options)
        try:
            command = ui.args[0]
        except:
            command = None

        if command is None:
            sys.exit(0)
        backup.validateCommand(command)
        ui.popArg()
        getattr(backup, 'cmd_%s' % command)(ui.args)
    except Exception, e:
        ui.handleError(e)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
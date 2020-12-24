# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\mm.py
# Compiled at: 2009-03-24 20:56:20
""" Backup for MindMeister mindmaps

    Dependencies:
     - module yaml   (available @ http://pyyaml.org/wiki/PyYAML)

"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mm.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $'
import sys, logging, os.path
from types import *
from optparse import OptionParser
levelsUp = 3
path = os.path.abspath(__file__)
while levelsUp > 0:
    path = os.path.dirname(path)
    levelsUp = levelsUp - 1

sys.path.append(path)
import jld.api as api, jld.registry as reg
from jld.backup.mindmeister_backup import Backup
import jld.backup.mindmeister_messages as msg, jld.backup.mindmeister_ui as mui, jld.backup.mindmeister_defaults as mdef
from jld.tools.template import ExTemplate
import jld.tools.logger as mlogger
_options = [{'o1': '-s', 'var': 'secret', 'action': 'store', 'help': 'config_secret', 'reg': True, 'default': None}, {'o1': '-k', 'var': 'api_key', 'action': 'store', 'help': 'config_key', 'reg': True, 'default': None}, {'o1': '-f', 'var': 'db_path', 'action': 'store', 'help': 'config_file', 'reg': True, 'default': None}, {'o1': '-p', 'var': 'export_path', 'action': 'store', 'help': 'config_path', 'reg': True, 'default': None}, {'o1': '-z', 'var': 'eventmgr_path', 'action': 'store', 'help': 'config_eventmgr', 'reg': True, 'default': None}, {'o1': '-m', 'var': 'export_maxnum', 'action': 'store', 'help': 'config_maxnum', 'reg': True, 'default': None, 'type': 'int'}, {'o1': '-l', 'var': 'syslog', 'action': 'store_true', 'help': 'syslog', 'reg': False, 'default': False}]

def main():
    msgs = msg.MM_Messages()
    ui = mui.MM_UI()
    ui.setParams(msgs)
    try:
        backup = Backup()
        usage_template = "%prog [options] command\n    \nversion $Id: mm.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $ by Jean-Lou Dupont\n\n*** Interface to MindMeister (http://www.mindmeister.com/) ***\nThis command-line utility requires valid 'API_KEY' and 'SECRET' parameters\nobtained from MindMeister. In order to use this tool, the 'auth' command\nmust first be called with the said valid parameters.\n\nUsage:\n Step 1) Authentication: use the 'auth' command with the '-s' and '-k' parameters\n Step 2) Update local database: use the 'updatedb' command to retrieve/update the local map database\n Step 3) Export: use the 'export' command to retrieve new maps / update existing ones \n\nThe commands which generate log entries are flagged with (logged) below.\n\nCommands:\n^^{commands}"
        commands_help = backup.genCommandsHelp()
        tpl = ExTemplate(usage_template)
        usage = tpl.substitute({'commands': commands_help})
        ui.handleArguments(usage, _options)
        _syslog = False if ui.options.syslog else True
        logger = mlogger.logger('mm', include_console=False, include_syslog=_syslog)
        backup.logger = logger
        ui.logger = logger
        r = reg.Registry('mindmeister')
        ui.updateRegistry(r, _options, ui.options)
        params = {}
        ui.integrateOptions(ui.options, params, _options)
        defs = mdef.MM_Defaults()
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
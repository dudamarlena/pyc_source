# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\gliffy.py
# Compiled at: 2009-03-24 20:56:20
""" Backup for Gliffy diagrams
    @author: Jean-Lou Dupont
    
     1. Scans the Delicious database for entries with the I{my-diagrams} tag
     2. Imports the 'ids' in the Gliffy database
     3. Searches for diagrams that haven't been exported
     4. Retrieves the diagrams through HTTP
     5. Writes the diagrams (all representations) to the export folder
     6. Updates the Gliffy database with the export information (i.e. time of export)
    
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: gliffy.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $'
import sys, logging, os.path
from types import *
from optparse import OptionParser
levelsUp = 3
path = os.path.abspath(__file__)
while levelsUp > 0:
    path = os.path.dirname(path)
    levelsUp = levelsUp - 1

sys.path.append(path)
import jld.api as api, jld.registry as reg, jld.backup.gliffy_messages as msg, jld.backup.gliffy_ui as dui, jld.backup.gliffy_defaults as ddef
from jld.backup.gliffy_backup import Backup
from jld.tools.template import ExTemplate
import jld.tools.logger as dlogger
_options = [{'o1': '-d', 'var': 'dlc_db_path', 'action': 'store', 'help': 'config_dlc_db_file', 'reg': True, 'default': None}, {'o1': '-g', 'var': 'glf_db_path', 'action': 'store', 'help': 'config_glf_db_file', 'reg': True, 'default': None}, {'o1': '-p', 'var': 'export_path', 'action': 'store', 'help': 'config_export_path', 'reg': True, 'default': None}, {'o1': '-m', 'var': 'export_maxnum', 'action': 'store', 'help': 'config_export_maxnum', 'reg': True, 'default': None, 'type': 'int'}, {'o1': '-l', 'var': 'syslog', 'action': 'store_true', 'help': 'syslog', 'reg': False, 'default': False}]

def main():
    msgs = msg.Gliffy_Messages()
    ui = dui.Gliffy_UI()
    ui.setParams(msgs)
    try:
        backup = Backup()
        usage_template = "%prog [options] command\n    \nversion $Id: gliffy.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $ by Jean-Lou Dupont\n\n*** Backup utility for Gliffy diagrams (http://www.gliffy.com/) ***\n\nUsage Notes:\n 1- This command line utility is meant to complement the cousin 'dlc' command line\n 2- The command 'import' is used to import bookmarks from the dlc (Delicious) database\n    The command 'import' is to be used with a parameter that denotes the 'tag' used to bookmark the Gliffy diagrams. \n    E.g. glf import my-diagrams\n     Will import from the dlc database all the bookmarks tagged with 'my-diagrams'.\n 3- The command 'export' is used to retrieve the diagrams from Gliffy.    \n\nThe commands which generate log entries are flagged with (logged) below.\n\nCommands:\n^^{commands}"
        commands_help = backup.genCommandsHelp()
        tpl = ExTemplate(usage_template)
        usage = tpl.substitute({'commands': commands_help})
        ui.handleArguments(usage, _options)
        _syslog = False if ui.options.syslog else True
        logger = dlogger.logger('glf', include_console=False, include_syslog=_syslog)
        backup.logger = logger
        ui.logger = logger
        r = reg.Registry('gliffy')
        ui.updateRegistry(r, _options, ui.options)
        params = {}
        ui.integrateOptions(ui.options, params, _options)
        defs = ddef.Gliffy_Defaults()
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
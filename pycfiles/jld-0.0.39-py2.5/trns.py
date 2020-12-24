# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\cmd_g2\transmission\trns.py
# Compiled at: 2009-03-24 20:56:20
"""
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: trns.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $'
import sys, logging, os.path
from types import *
from optparse import OptionParser
import jld.registry as reg
from jld.tools.ytools import Yattr, Ymsg
from jld.cmd_g2.base_ui import BaseCmdUI
from jld.tools.template import ExTemplate
import jld.tools.logger as _logger
from cmd import TransmissionCmd
_options = [{'o1': '-s', 'var': 'config_server', 'action': 'store', 'help': 'config_server', 'reg': True, 'default': None, 'type': 'string'}, {'o1': '-p', 'var': 'config_port', 'action': 'store', 'help': 'config_port', 'reg': True, 'default': None}, {'o1': '-l', 'var': 'config_syslog', 'action': 'store_true', 'help': 'config_syslog', 'reg': False, 'default': False}, {'o1': '-e', 'var': 'config_export', 'action': 'store_true', 'help': 'config_export', 'reg': False, 'default': False}, {'o1': '-a', 'var': 'config_autostop', 'action': 'store_true', 'help': 'config_autostop', 'reg': False, 'default': False}, {'o1': '-z', 'var': 'config_eventmgr', 'action': 'store', 'help': 'config_eventmgr', 'reg': True, 'default': None, 'type': 'string'}]

def main():
    msgs = Ymsg(__file__)
    defaults = Yattr(__file__)
    ui = BaseCmdUI(msgs)
    try:
        cmd = TransmissionCmd()
        cmd.msgs = msgs
        usage_template = '%prog [options] command\n    \nversion $Id: trns.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $ by Jean-Lou Dupont\n\n*** Interface to Transmission (Bittorent client) ***\nProvides the capability to verify the status of each active torrent,\nexport its status upon completion (useful for post-processing) and\nautomatically stopping a torrent after completion.\n\nCommands:\n^^{commands}'
        tpl = ExTemplate(usage_template)
        usage = tpl.substitute({'commands': cmd.commands_help})
        ui.handleArguments(usage, _options)
        _syslog = ui.options.config_syslog
        logger = _logger.logger('trns', include_console=False, include_syslog=_syslog)
        cmd.logger = logger
        ui.logger = logger
        r = reg.Registry('trns')
        ui.updateRegistry(r, _options, ui.options)
        params = {}
        ui.integrateOptions(ui.options, params, _options)
        ui.integrateDefaults(defaults, r, _options, params)
        ui.verifyType(params, _options)
        ui.copyOptions(params, cmd, _options)
        if ui.command is None:
            sys.exit(0)
        cmd.validateCommand(ui.command)
        ui.popArg()
        getattr(cmd, 'cmd_%s' % ui.command)(ui.args)
    except Exception, e:
        ui.handleError(e)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\backup\mmd.py
# Compiled at: 2008-12-12 20:05:34
""" 
    MindMeister backup daemon
    @author: Jean-Lou Dupont
    
    Prerequisites:
     - the keys 'secret', 'api_key' and 'file' be properly set in the registry.
       This filesystem path points to the Sqlite database used to
       store the map related information.
      
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mmd.py 729 2008-12-11 18:30:12Z jeanlou.dupont $'
import os, sys, signal
levelsUp = 3
path = os.path.abspath(__file__)
while levelsUp > 0:
    path = os.path.dirname(path)
    levelsUp = levelsUp - 1

sys.path.append(path)
import jld.tools.daemon as daemon

class mmdDaemon(daemon.BaseDaemon):
    """ Daemon
    """
    _name = 'mmd'

    def __init__(self):
        daemon.BaseDaemon.__init__(self, mmdDaemon._name)

    def run(self):
        """
        """
        self.loginfo('mmd: default run()')
        while True:
            signal.pause()


import jld.tools.cmd_ui as ui

class mmdUI(ui.UIBase):
    """ Handles user interface
    """
    _map = {'jld.api.ErrorDaemon': {'msg': 'error_daemon', 'help': 'help_daemon'}, 'jld.api.ErrorDb': {'msg': 'error_db', 'help': 'help_db'}, 'jld.api.ErrorAuth': {'msg': 'error_auth', 'help': 'help_auth'}, 'jld.api.ErrorNetwork': {'msg': 'error_network', 'help': 'help_network'}, 'jld.api.ErrorAccess': {'msg': 'error_access', 'help': 'help_access'}, 'jld.api.ErrorMethod': {'msg': 'error_method', 'help': 'help_method'}, 'jld.api.ErrorValidation': {'msg': 'error_validation', 'help': 'help_validation'}, 'jld.api.ErrorProtocol': {'msg': 'error_protocol', 'help': 'help_protocol'}, 'jld.api.ErrorInvalidCommand': {'msg': 'error_command', 'help': 'help_command'}, 'jld.registry.exception.RegistryException': {'msg': 'error_registry', 'help_win': 'help_registry_win', 'help_nix': 'help_registry_nix'}}


import os.path
from jld.tools.messages import Messages

class mmdMessages(Messages):
    """ Messages
    """
    filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'mindmeister_messages.yaml'

    def __init__(self):
        Messages.__init__(self, self.filepath)


from jld.cmd import BaseCmd

class mmdCmd(BaseCmd):
    """ Handles the command line interface of this daemon
    """

    def __init__(self, daemon, msgs):
        BaseCmd.__init__(self)
        self.daemon = daemon
        self.msgs = msgs
        self.quiet = False

    def cmd_start(self, *args):
        """ Starts the daemon """
        self._sendMsg('daemon_start')
        childpid = self.daemon.start()

    def cmd_stop(self, *args):
        """ Stops the daemon """
        self._sendMsg('daemon_stop')
        self.daemon.stop()

    def cmd_restart(self, *args):
        """ Restarts the daemon """
        self._sendMsg('daemon_restart')
        self.daemon.restart()

    def _sendMsg(self, msg, params=None):
        if not self.quiet:
            print self.msgs.render(msg, params)


from jld.tools.template import ExTemplate

def main():
    """ Entry point
        - Performs command line processing
        -- start:   verifies required configuration
        -- stop:    finds process, sends TERM
        -- restart: performs stop, performs start
    """
    msgs = mmdMessages()
    ui = mmdUI()
    ui.setParams(msgs)
    try:
        daemon = mmdDaemon()
        cmd = mmdCmd(daemon, msgs)
        usage_template = '%prog [options] command\n    \nversion $Id: mmd.py 729 2008-12-11 18:30:12Z jeanlou.dupont $ by Jean-Lou Dupont\n\n*** Interface to MindMeister (http://www.mindmeister.com/) ***\n\nCommands:\n^^{commands}'
        commands_help = cmd.genCommandsHelp()
        tpl = ExTemplate(usage_template)
        usage = tpl.substitute({'commands': commands_help})
        _options = [{'o1': '-q', 'var': 'quiet', 'action': 'store_true', 'help': 'quiet', 'reg': False, 'default': False}]
        ui.handleArguments(usage, _options)
        try:
            command = ui.args[0]
        except:
            command = None

        cmd.validateCommand(command)
        ui.popArg()
        cmd.quiet = getattr(ui.options, 'quiet')
        getattr(cmd, 'cmd_%s' % command)(ui.args)
    except Exception, e:
        ui.handleError(e)

    return


if __name__ == '__main__':
    main()
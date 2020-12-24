# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/main.py
# Compiled at: 2018-01-03 10:08:36
import logging, sys
from cliff import app
from cliff.commandmanager import CommandManager
LOG = logging.getLogger(__name__)

class GerritClient(app.App):
    """Main cliff application class.

    Initialization of the command manager and configuration of basic engines.
    """

    def run(self, argv):
        return super(GerritClient, self).run(argv)


def main(argv=sys.argv[1:]):
    gerritclient_app = GerritClient(description='CLI tool for managing Gerrit Code Review.', version='0.1.0', command_manager=CommandManager('gerritclient', convert_underscores=True), deferred_help=True)
    return gerritclient_app.run(argv)


def debug(name, cmd_class, argv=None):
    """Helper for debugging single command without package installation."""
    import sys
    if argv is None:
        argv = sys.argv[1:]
    argv = [name] + argv + ['-v', '-v', '--debug']
    cmd_mgr = CommandManager('test_gerritclient', convert_underscores=True)
    cmd_mgr.add_command(name, cmd_class)
    return GerritClient(description='CLI tool for managing Gerrit Code Review.', version='0.1.0', command_manager=cmd_mgr).run(argv)
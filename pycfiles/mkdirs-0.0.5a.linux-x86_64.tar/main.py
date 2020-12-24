# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mkdirs/main.py
# Compiled at: 2014-10-01 14:18:24
import logging, sys
from cliff.app import App
from cliff.commandmanager import CommandManager

class MkDirsApp(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(MkDirsApp, self).__init__(description='CLI for auto-scaffolding cliff based project', version='0.0.5a', command_manager=CommandManager('mkdirs.app'))

    def initialize_app(self, argv):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare to run command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    mker = MkDirsApp()
    return mker.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
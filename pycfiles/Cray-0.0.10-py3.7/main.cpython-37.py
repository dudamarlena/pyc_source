# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cray/commands/main.py
# Compiled at: 2020-03-04 04:13:49
# Size of source mod 2**32: 850 bytes
import sys
from cliff.app import App
from cliff.commandmanager import CommandManager

class Cray(App):

    def __init__(self):
        super(Cray, self).__init__(description='CLI for batch processing system',
          version='0.0.10',
          command_manager=(CommandManager('cray')),
          deferred_help=True)

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    c = Cray()
    return c.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
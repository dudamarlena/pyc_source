# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bdx/.virtualenvs/mkdirstest/lib/python2.7/site-packages/crepopy/main.py
# Compiled at: 2014-10-29 21:25:29
import logging, sys
from cliff.app import App
from cliff.commandmanager import CommandManager

class Crepopy(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(Crepopy, self).__init__(description='Crepopy', version='0.1', command_manager=CommandManager('crepopy.app'))

    def initialize_app(self, argv):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = Crepopy()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
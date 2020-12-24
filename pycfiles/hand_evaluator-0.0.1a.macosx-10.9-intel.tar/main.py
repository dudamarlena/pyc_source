# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/WorkHD/Users/jbeedy/.virtualenvs/evaluator/lib/python2.7/site-packages/evaluator/main.py
# Compiled at: 2014-11-06 19:19:53
import logging, sys
from cliff.app import App
from cliff.commandmanager import CommandManager

class Evaluator(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(Evaluator, self).__init__(description='Evaluator', version='0.1', command_manager=CommandManager('evaluator.app'))

    def initialize_app(self, argv):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = Evaluator()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
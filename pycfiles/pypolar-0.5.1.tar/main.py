# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bdx/.virtualenvs/pypoker/lib/python2.7/site-packages/evaluator/main.py
# Compiled at: 2014-10-07 12:43:59
import logging, sys
from cliff.app import App
from cliff.commandmanager import CommandManager

class PyPoker(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(PyPoker, self).__init__(description='CLI for evaluating poker hands', version='0.0.1a', command_manager=CommandManager('pypoker.app'))

    def initialize_app(self, argv):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare to run command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = PyPoker()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
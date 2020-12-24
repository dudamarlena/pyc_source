# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/commands/test.py
# Compiled at: 2020-04-09 09:23:00
# Size of source mod 2**32: 884 bytes
import logging
from squad_client.core.command import SquadClientCommand
INCLUDE_TESTS_CMD = True
logger = logging.getLogger()
try:
    import tests
except ImportError:
    INCLUDE_TESTS_CMD = False

class TestCommand(SquadClientCommand):
    command = 'test'
    help_text = 'test squad_client code'

    def register(self, subparser):
        if not INCLUDE_TESTS_CMD:
            return False
        parser = super(TestCommand, self).register(subparser)
        parser.add_argument('tests', nargs='*', help='list of tests to run')
        parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true', default=False)
        parser.add_argument('--coverage', help='run tests with coverage', action='store_true', default=False)

    def run(self, args):
        logger.info('Running tests')
        return tests.run(args.coverage, args.tests, args.verbose)
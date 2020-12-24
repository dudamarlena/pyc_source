# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/squad_client/commands/test.py
# Compiled at: 2020-02-22 16:13:46
# Size of source mod 2**32: 898 bytes
import sys, os
from squad_client.core.command import SquadClientCommand
import tests

class TestCommand(SquadClientCommand):
    command = 'test'
    help_text = 'test squad_client code'

    def register(self, subparser):
        parser = super(TestCommand, self).register(subparser)
        parser.add_argument('tests', nargs='*', help='list of tests to run')
        parser.add_argument('--coverage', help='run tests with coverage', action='store_true', default=False)

    def run(self, args):
        print('Running tests')
        if args.coverage:
            print('\t --coverage is enabled, run `coverage report -m` to view coverage report')
            argv = [
             'coverage', 'run', '--source', 'squad_client', '-m', 'unittest', 'discover']
            return os.execvp('coverage', argv)
        tests.run()
        return True
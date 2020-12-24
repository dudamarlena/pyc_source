# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/squad_client/commands/shell.py
# Compiled at: 2020-03-05 18:07:33
# Size of source mod 2**32: 816 bytes
import sys, os, IPython
from squad_client.core.command import SquadClientCommand

class ShellCommand(SquadClientCommand):
    command = 'shell'
    help_text = 'run squad-client on shell'

    def register(self, subparser):
        parser = super(ShellCommand, self).register(subparser)
        parser.add_argument('script', nargs='?', help='python script to run')

    def run(self, args):
        if args.script:
            with open(args.script, 'r') as (script_source):
                try:
                    program = compile(script_source.read(), args.script, 'exec')
                except SyntaxError as e:
                    try:
                        print('Cannot run "%s": %s' % (args.script, e))
                    finally:
                        e = None
                        del e

            exec(program)
            return True
        IPython.embed()
        return True
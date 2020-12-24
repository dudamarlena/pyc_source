# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/commands/shell.py
# Compiled at: 2020-04-09 09:23:00
# Size of source mod 2**32: 1055 bytes
import IPython, logging, sys
from squad_client.core.command import SquadClientCommand
logger = logging.getLogger()

class ShellCommand(SquadClientCommand):
    command = 'shell'
    help_text = 'run squad-client on shell'

    def register(self, subparser):
        parser = super(ShellCommand, self).register(subparser)
        parser.add_argument('script', nargs='?', help='python script to run')
        parser.add_argument('--script-params', dest='script_params', help='script parameters')

    def run(self, args):
        if args.script:
            with open(args.script, 'r') as (script_source):
                try:
                    program = compile(script_source.read(), args.script, 'exec')
                except SyntaxError as e:
                    logger.error('Cannot run "%s": %s' % (args.script, e))
                    return False

            sys.argv = [
             args.script] + args.script_params.split(' ')
            exec(program)
            return True
        else:
            IPython.embed()
            return True
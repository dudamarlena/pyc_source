# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo89/mogo/term/terminal/commands.py
# Compiled at: 2017-12-26 07:14:55
# Size of source mod 2**32: 450 bytes
from term.commands import Command, rprint

def thelp(request, cmd_args):
    from term.apps import ALLCMDS
    for appname in ALLCMDS:
        cmds = ALLCMDS[appname]
        for cmd in cmds:
            if cmd.name != 'help':
                rprint('<em>', cmd.name, '</em>:', cmd.help)


def ping(request, cmd_args):
    rprint('PONG')


c0 = Command('help', thelp, 'Terminal help')
c1 = Command('ping', ping, 'Ping server')
COMMANDS = [
 c0, c1]
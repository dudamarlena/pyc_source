# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/output.py
# Compiled at: 2013-05-15 07:26:23
import os, sys, inspect, mico
from mico.lib.core.local import is_local
intros = [
 'the monkey army for the cloud',
 'just see! a monkey flying in the cloud',
 'uuuh uhuh uhuhuhuhu uh uh uh!',
 'the monkey driven cloud management',
 'oh no! monkys are learning to fly!',
 'take your stinking paws off me, you dammed dirty ape!']
monkey = '\n             .--.  .-"     "-.  .--.\n            / .. \\/  .-. .-.  \\/ .. \\\n           | |  \'|  /   Y   \\  |\'  | |\n           | \\   \\  \\ 0 | 0 /  /   / |\n            \\ \'- ,\\.-"`` ``"-./, -\' /\n             `\'-\' /_   ^ ^   _\\ \'-\'`\n             .--\'|  \\._   _./  |\'--.\n           /`    \\   \\ `~` /   /    `\\ \n          /       \'._ \'---\' _.\'       \\\n         /           \'~---~\'   |       \\\n        /        _.             \\       \\\n       /   .\'-./`/        .\'~\'-.|\\       \\\n      /   /    `\\:       /      `\'.      \\\n     /   |       ;      |         \'.`;    /\n     \\   \\       ;      \\           \\/   /\n      \'.  \\      ;       \\       \\   `  /\n        \'._\'.     \\       \'.      |   ;/_\n          /__>     \'.       \\_ _ _/   ,  \'--.\n        .\'   \'.   .-~~~~~-. /     |--\'`~~-.  \\\n       // / .---\'/  .-~~-._/ / / /---..__.\'  /\n      ((_(_/    /  /      (_(_(_(---.__    .\'\n                | |     _              `~~`\n                | |     \\\'.\n                 \\ \'....\' |\n                  \'.,___.\'\n'
prompt_usr = os.environ.get('MICO_PS1', None) or '\x1b[0;1mmico\x1b[1;34m:\x1b[0;0m '
prompt_err = os.environ.get('MICO_PS2', None) or '\x1b[31;1mmico\x1b[0;1m:\x1b[0;0m '
prompt_inf = os.environ.get('MICO_PS3', None) or '\x1b[33;1mmico\x1b[0;1m:\x1b[0;0m '
prompt_msg = os.environ.get('MICO_PS4', None) or '\x1b[34;1mmico\x1b[0;1m:\x1b[0;0m '
prompt_dbg = os.environ.get('MICO_PS4', None) or '\x1b[30;1mmico\x1b[0;1m:\x1b[0;0m '
env.loglevel = set(['abort', 'error', 'warn', 'info'])

def abort(message):
    if 'abort' in env.loglevel:
        _h = env['host_string'] or ('local' if is_local() else 'cloud')
        print >> sys.stderr, '%s\x1b[0;1m%s:\x1b[0;0m %s: %s' % (prompt_err,
         _h, inspect.stack()[1][3], message)


def error(message, func=None, exception=None, stdout=None, stderr=None):
    if 'error' in env.loglevel:
        _h = env['host_string'] or ('local' if is_local() else 'cloud')
        print >> sys.stderr, '%s\x1b[0;1m%s:\x1b[0;0m %s: %s' % (prompt_err,
         _h, inspect.stack()[1][3], exception or message)


def warn(message):
    if 'warn' in env.loglevel:
        _h = env['host_string'] or ('local' if is_local() else 'cloud')
        print >> sys.stderr, '%s\x1b[0;1m%s:\x1b[0;0m %s: %s' % (prompt_inf,
         _h, inspect.stack()[1][3], message)


def puts(text, show_prefix=None, end='\n', flush=False):
    if 'info' in env.loglevel:
        _h = env['host_string'] or ('local' if is_local() else 'cloud')
        print >> sys.stderr, '%s\x1b[0;1m%s:\x1b[0;0m %s: %s' % (prompt_inf,
         _h, inspect.stack()[1][3], text)


def info(message):
    if 'info' in env.loglevel:
        _h = env['host_string'] or ('local' if is_local() else 'cloud')
        print >> sys.stdout, '%s\x1b[0;1m%s:\x1b[0;0m %s: %s' % (prompt_msg,
         _h, inspect.stack()[1][3], message)


def debug(message):
    if 'debug' in env.loglevel:
        _h = env['host_string'] or ('local' if is_local() else 'cloud')
        print >> sys.stdout, '%s\x1b[0;1m%s:\x1b[0;0m %s: %s' % (prompt_dbg,
         _h, inspect.stack()[1][3], message)


def mute(*args, **kwargs):
    pass


from fabric.state import output
output['debug'] = False
output['running'] = False
output['stderr'] = False
output['stdout'] = False
output['status'] = False
import fabric.tasks, fabric.utils, fabric.operations
fabric.operations.abort = fabric.utils.abort = fabric.tasks.abort = abort
fabric.operations.error = fabric.utils.error = fabric.tasks.error = mute
fabric.operations.warn = fabric.utils.warn = fabric.tasks.warn = mute
fabric.operations.puts = fabric.utils.puts = fabric.utils.puts = mute
fabric.operations.fastprint = fabric.utils.fastprint = fabric.utils.fastprint = puts
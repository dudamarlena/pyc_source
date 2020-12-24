# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/pid.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 551 bytes
"""
Print the process ID of the current bp instance that is running a project,
if any.

DEPRECATED: use ``$ bpa-pid``
"""
DESCRIPTION = '\nExample:\n\n.. code-block:: bash\n\n    $ bp pid\n\n'
from ..util import log, pid_context

def run(args):
    try:
        log.printer(pid_context.get_pid(args.pid_filename))
    except:
        log.error('No bp process running')
        log.debug('Could not find file %s', args.pid_filename)
        return -1


def add_arguments(parser):
    pid_context.add_arguments(parser)
    parser.set_defaults(run=run)
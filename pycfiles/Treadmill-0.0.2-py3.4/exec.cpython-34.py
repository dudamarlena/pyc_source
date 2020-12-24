# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/exec.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 486 bytes
"""Exec command in Treadmill sproc environment."""
import os, logging, click
_LOGGER = logging.getLogger(__name__)

def init():
    """Top level command handler."""

    @click.command(name='exec')
    @click.argument('cmd', nargs=-1)
    def exec_cmd(cmd):
        """Exec command line in treadmill environment."""
        args = list(cmd)
        print(args)
        _LOGGER.info('execvp: %s, %r', args[0], args)
        os.execvp(args[0], args)

    return exec_cmd
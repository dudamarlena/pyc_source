# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.dennis/development/ship_it/ship_it/cli.py
# Compiled at: 2018-07-05 16:56:37
# Size of source mod 2**32: 1665 bytes
from __future__ import unicode_literals
import pipes
from os import path
import invoke

def invoke_fpm(command_line):
    cmd = 'fpm -f -s dir -t rpm {}'.format(command_line)
    invoke.run(cmd)


def format_flags(flags):
    for flag, value in flags:
        if value not in ('', None):
            quoted_value = pipes.quote(str(value))
            quoted_value = ' ' + quoted_value
        else:
            quoted_value = ''
        if not flag or flag.count('-') == len(flag):
            raise ValueError('illegal flag: {!r} in {!r}'.format(flag, flags))
        if flag.startswith('--'):
            if len(flag) == 3:
                yield '{}{}'.format(flag[1:], quoted_value)
            else:
                yield '{}{}'.format(flag, quoted_value)
        else:
            if flag.startswith('-'):
                if len(flag) == 2:
                    yield '{}{}'.format(flag, quoted_value)
                else:
                    yield '-{}{}'.format(flag, quoted_value)
            else:
                if len(flag) == 1:
                    yield '-{}{}'.format(flag, quoted_value)
                else:
                    yield '--{}{}'.format(flag, quoted_value)


def get_command_line(args, flags):
    return '{} {}'.format(' '.join(format_flags(flags)), ' '.join(pipes.quote(arg) for arg in args))
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.dennis/development/ship_it/ship_it/cli.py
# Compiled at: 2018-07-05 16:56:37
from __future__ import unicode_literals
import pipes
from os import path
import invoke

def invoke_fpm(command_line):
    cmd = (b'fpm -f -s dir -t rpm {}').format(command_line)
    invoke.run(cmd)


def format_flags(flags):
    for flag, value in flags:
        if value not in ('', None):
            quoted_value = pipes.quote(str(value))
            quoted_value = b' ' + quoted_value
        else:
            quoted_value = b''
        if not flag or flag.count(b'-') == len(flag):
            raise ValueError((b'illegal flag: {!r} in {!r}').format(flag, flags))
        if flag.startswith(b'--'):
            if len(flag) == 3:
                yield (b'{}{}').format(flag[1:], quoted_value)
            else:
                yield (b'{}{}').format(flag, quoted_value)
        elif flag.startswith(b'-'):
            if len(flag) == 2:
                yield (b'{}{}').format(flag, quoted_value)
            else:
                yield (b'-{}{}').format(flag, quoted_value)
        elif len(flag) == 1:
            yield (b'-{}{}').format(flag, quoted_value)
        else:
            yield (b'--{}{}').format(flag, quoted_value)

    return


def get_command_line(args, flags):
    return (b'{} {}').format((b' ').join(format_flags(flags)), (b' ').join(pipes.quote(arg) for arg in args))
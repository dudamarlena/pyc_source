# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/optval.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import unicode_literals
import getopt

class InvalidOptionArgument(Exception):

    def __init__(self, msg):
        super(InvalidOptionArgument, self).__init__(msg)
        self.msg = msg


def __find_arg_in_options__(arg, options):
    for opt in options:
        if opt[0].find(arg) == 0:
            return opt

    return


def __find_options_to_extend__(long_options):
    options_to_extend = []
    for num, arg in enumerate(long_options):
        arg = arg.split(b':')
        if len(arg) == 2:
            long_options[num] = arg[0] + b'='
            options_to_extend.append((b'--' + arg[0], arg[1]))

    return options_to_extend


def gnu_getopt(args, options, long_options):
    options_to_extend = __find_options_to_extend__(long_options)
    for num, arg in enumerate(args):
        opt = __find_arg_in_options__(arg, options_to_extend)
        if opt:
            args[num] = arg + b'=' + opt[1]

    return getopt.gnu_getopt(args, options, long_options)


def get_boolean_argument(arg):
    if isinstance(arg, bool):
        return arg
    else:
        if arg == None or arg.lower() == b'false' or arg.lower() == b'f' or arg == b'0':
            return False
        if arg.lower() == b'true' or arg.lower() == b't' or arg == b'1':
            return True
        raise InvalidOptionArgument(_(b'The given option argument is not a valid boolean.'))
        return
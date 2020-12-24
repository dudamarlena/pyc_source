# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/deprecated.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2109 bytes
import os, sys
CHOICES = ('ignore', 'fail', 'warn', 'warn_once')
DEFAULT = 'warn_once'
ACTION = None
HELP = '\nSpecify what to do when a project uses deprecated features:\n\n  ignore: do nothing\n  warn: print warning messages for each feature\n  warn_once: print a warning message, but only once for each type of feature\n  fail: throw an exception\n'
DEPRECATED = set()
FLAG = '--deprecated'
V4_FLAG = '--v4'
ENVIRONMENT_VARIABLE = 'BP_DEPRECATED'
V4_HELP = 'Run BiblioPixel in v4 compatibility mode, to see if it will work with\nfuture releases v4.x\n'

def add_arguments(parser):
    parser.add_argument(V4_FLAG, action='store_true', help=V4_HELP)


def allowed():
    global ACTION
    _compute_action()
    return ACTION != 'fail'


def deprecated(msg, *args, **kwds):
    _compute_action()
    if ACTION == 'ignore':
        return
    if ACTION == 'warn_once':
        if msg in DEPRECATED:
            return
    formatted = (msg.format)(*args, **kwds)
    if ACTION == 'fail':
        raise ValueError(formatted)
    DEPRECATED.add(msg)
    from . import log
    log.warning(formatted)


def _compute_action():
    global ACTION
    if ACTION:
        return
    else:
        if FLAG in sys.argv:
            raise ValueError('%s needs an argument (one of %s)' % (
             FLAG, ', '.join(CHOICES)))
        else:
            if V4_FLAG in sys.argv:
                ACTION = 'fail'
            else:
                d = [i for i, v in enumerate(sys.argv) if v.startswith(FLAG + '=')]
                if len(d) > 1:
                    raise ValueError('Only one %s argument can be used' % FLAG)
                if not d:
                    ACTION = os.getenv(ENVIRONMENT_VARIABLE, ACTION or DEFAULT)
                else:
                    arg = sys.argv.pop(d[0])
                    _, *rest = arg.split('=')
                    if len(rest) > 1:
                        raise ValueError('Extra = in flag %s' % arg)
                    if not (rest and rest[0].strip()):
                        raise ValueError('%s needs an argument (one of %s)' % (
                         FLAG, ', '.join(CHOICES)))
            ACTION = rest[0]
        if ACTION not in CHOICES:
            ACTION = None
            raise ValueError('Unknown deprecation value (must be one of %s)' % ', '.join(CHOICES))
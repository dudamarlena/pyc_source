# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/util.py
# Compiled at: 2018-10-15 19:16:31
# Size of source mod 2**32: 2171 bytes
import os, stat

class memoize(dict):
    __doc__ = '\n    Basic memoizing class, taken from\n    http://wiki.python.org/moin/PythonDecoratorLibrary#Alternate_memoize_as_dict_subclass\n    '

    def __init__(self, func):
        self.func = func
        self.memoized = {}

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = (self.func)(*key)
        return result


def is_pipe(file_obj):
    return stat.S_ISFIFO(os.fstat(file_obj.fileno()).st_mode)


def add_atom_selection_arguments(parser):
    parser.add_argument('--only-CA', action='store_true',
      default=False,
      help='Only use C-alpha atoms.')
    parser.add_argument('--only-backbone', action='store_true',
      default=False,
      help='Only use backbone atoms.')
    parser.add_argument('--only-selection', default=None,
      help='Use ProDy selection to select atoms.')
    return parser


def _is_string_like(obj):
    """
    Check whether obj behaves like a string.
    """
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    else:
        return True


def which(program, required=False):
    """Find an executable.

    Replicates the behavior of the 'which' shell built-in command. If no
    executable is found, returns None.
    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    if required:
        raise FileNotFoundError(program)


def compare_cache():
    pass
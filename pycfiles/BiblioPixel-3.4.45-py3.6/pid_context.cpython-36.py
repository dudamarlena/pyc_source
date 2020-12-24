# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/pid_context.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1370 bytes
import contextlib, os, tempfile
from . import log
DEFAULT_PID_FILENAME = os.path.join(tempfile.gettempdir(), 'bp_pid_file.txt')
HELP = 'Filename to store the `bp` process ID when running'

def add_arguments(parser):
    parser.add_argument('--pid_filename',
      default=DEFAULT_PID_FILENAME, help=HELP)


@contextlib.contextmanager
def pid_context(pid_filename=None):
    """
    For the duration of this context manager, put the PID for this process into
    `pid_filename`, and then remove the file at the end.
    """
    pid_filename = pid_filename or DEFAULT_PID_FILENAME
    if os.path.exists(pid_filename):
        contents = open(pid_filename).read(16)
        log.warning('pid_filename %s already exists with contents %s', pid_filename, contents)
    with open(pid_filename, 'w') as (fp):
        fp.write(str(os.getpid()))
        fp.write('\n')
    try:
        yield
    finally:
        try:
            os.remove(pid_filename)
        except Exception as e:
            log.error('Got an exception %s deleting the pid_filename %s', e, pid_filename)


def get_pid(pid_filename=None):
    """
    Return the integer PID for the current bp process, or raise an exception if
    there is no such process or it hasn't registered a PID.
    """
    return int(open(pid_filename or DEFAULT_PID_FILENAME).read(16))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongotail/err.py
# Compiled at: 2019-02-06 07:01:12
# Size of source mod 2**32: 1888 bytes
import sys
from errno import EINVAL, EINTR, ECONNREFUSED, EFAULT, EDESTADDRREQ

def warn(msg):
    sys.stderr.write('Mongotail EXCEPTION - %s\n' % msg)
    sys.stderr.flush()


def error(msg, exit_code):
    """
    Print `msg` error and exit with status `exit_code`
    """
    sys.stderr.write("%s\ntry 'mongotail --help' for more information\n" % msg)
    sys.stderr.flush()
    exit(exit_code)


def error_parsing(msg='unknown options'):
    """
    Print any parsing error and exit with status -1
    """
    sys.stderr.write("Error parsing command line: %s\ntry 'mongotail --help' for more information\n" % msg)
    sys.stderr.flush()
    exit(EINVAL)


def error_unknown():
    """
    Print an unexpected error and exit with status -5
    """
    sys.stderr.write("Unknown Error\ntry 'mongotail --help' for more information\n")
    sys.stderr.flush()
    exit(-1)
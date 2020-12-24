# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/checks.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
import os, subprocess
from rbtools.utils.process import execute
GNU_DIFF_WIN32_URL = b'http://gnuwin32.sourceforge.net/packages/diffutils.htm'

def check_install(command):
    """Check if the given command is installed.

    Try executing an external command and return a boolean indicating whether
    that command is installed or not.  The 'command' argument should be
    something that executes quickly, without hitting the network (for
    instance, 'svn help' or 'git --version').
    """
    try:
        subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (OSError, ValueError):
        return False


def check_gnu_diff():
    """Checks if GNU diff is installed, and informs the user if it's not."""
    has_gnu_diff = False
    try:
        if hasattr(os, b'uname') and os.uname()[0] == b'SunOS':
            diff_cmd = b'gdiff'
        else:
            diff_cmd = b'diff'
        result = execute([diff_cmd, b'--version'], ignore_errors=True)
        has_gnu_diff = b'GNU diffutils' in result
    except OSError:
        pass

    if not has_gnu_diff:
        error = b'GNU diff is required in order to generate diffs. Make sure it is installed and in the path.\n'
        if os.name == b'nt':
            error += b'On Windows, you can install this from %s\n' % GNU_DIFF_WIN32_URL
        raise Exception(error)


def is_valid_version(actual, expected):
    """
    Takes two tuples, both in the form:
        (major_version, minor_version, micro_version)
    Returns true if the actual version is greater than or equal to
    the expected version, and false otherwise.
    """
    return actual[0] > expected[0] or actual[0] == expected[0] and actual[1] > expected[1] or actual[0] == expected[0] and actual[1] == expected[1] and actual[2] >= expected[2]
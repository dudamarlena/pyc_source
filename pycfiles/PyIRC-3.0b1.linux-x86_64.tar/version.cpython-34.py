# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/util/version.py
# Compiled at: 2015-10-08 05:15:50
# Size of source mod 2**32: 1660 bytes
"""PyIRC version information."""
try:
    import pkg_resources
except ImportError:
    pkg_resources = None

import subprocess
from collections import namedtuple

def _gitversion():
    """Determine the current git checkout, if any."""
    try:
        command = [
         'git', 'log', '-1', '--pretty=format:%h']
        return subprocess.check_output(command).decode()
    except (OSError, subprocess.SubprocessError):
        return 'UNKNOWN'


major = 3
minor = 0
status = 'alpha'
gitversion = _gitversion()
Version = namedtuple('Version', 'major minor status gitversion')
version = Version(major, minor, status, gitversion)

def _versionstr():
    """Create the version string from the current parameters."""
    try:
        req = pkg_resources.require('PyIRC')
        return req[0].version
    except pkg_resources.DistributionNotFound:
        return '{major}.{minor}-{status[0]}[{gitversion}]'.format(**globals())


versionstr = _versionstr()
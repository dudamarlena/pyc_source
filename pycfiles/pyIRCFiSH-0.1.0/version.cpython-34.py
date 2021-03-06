# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/util/version.py
# Compiled at: 2015-10-08 05:15:50
# Size of source mod 2**32: 1660 bytes
__doc__ = 'PyIRC version information.'
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
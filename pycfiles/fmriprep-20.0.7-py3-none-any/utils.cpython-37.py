# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/setuptools/setuptools/_vendor/packaging/utils.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 1520 bytes
from __future__ import absolute_import, division, print_function
import re
from .version import InvalidVersion, Version
_canonicalize_regex = re.compile('[-_.]+')

def canonicalize_name(name):
    return _canonicalize_regex.sub('-', name).lower()


def canonicalize_version(version):
    """
    This is very similar to Version.__str__, but has one subtle differences
    with the way it handles the release segment.
    """
    try:
        version = Version(version)
    except InvalidVersion:
        return version
    else:
        parts = []
        if version.epoch != 0:
            parts.append('{0}!'.format(version.epoch))
        parts.append(re.sub('(\\.0)+$', '', '.'.join((str(x) for x in version.release))))
        if version.pre is not None:
            parts.append(''.join((str(x) for x in version.pre)))
        if version.post is not None:
            parts.append('.post{0}'.format(version.post))
        if version.dev is not None:
            parts.append('.dev{0}'.format(version.dev))
        if version.local is not None:
            parts.append('+{0}'.format(version.local))
        return ''.join(parts)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/_version.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 4818 bytes
"""

Module for version handling:

provides:
* version = "1.2.3" or "1.2.3-beta4"
* version_info = named tuple (1,2,3,"beta",4)
* hexversion: 0x010203B4
* strictversion = "1.2.3b4
* debianversion = "1.2.3~beta4"

This is called hexversion since it only really looks meaningful when viewed as the
result of passing it to the built-in hex() function.
The version_info value may be used for a more human-friendly encoding of the same information.

The hexversion is a 32-bit number with the following layout:
Bits (big endian order)     Meaning
1-8     PY_MAJOR_VERSION (the 2 in 2.1.0a3)
9-16     PY_MINOR_VERSION (the 1 in 2.1.0a3)
17-24     PY_MICRO_VERSION (the 0 in 2.1.0a3)
25-28     PY_RELEASE_LEVEL (0xA for alpha, 0xB for beta, 0xC for release candidate and 0xF for final)
29-32     PY_RELEASE_SERIAL (the 3 in 2.1.0a3, zero for final releases)

Thus 2.1.0a3 is hexversion 0x020100a3.

"""
from __future__ import absolute_import, print_function, division
__author__ = 'Jerome Kieffer'
__contact__ = 'Jerome.Kieffer@ESRF.eu'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__date__ = '03/04/2020'
__status__ = 'production'
__docformat__ = 'restructuredtext'
RELEASE_LEVEL_VALUE = {'dev': 0, 
 'alpha': 10, 
 'beta': 11, 
 'gamma': 12, 
 'rc': 13, 
 'final': 15}
MAJOR = 0
MINOR = 10
MICRO = 0
RELEV = 'final'
SERIAL = 0
from collections import namedtuple
_version_info = namedtuple('version_info', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
version_info = _version_info(MAJOR, MINOR, MICRO, RELEV, SERIAL)
strictversion = version = debianversion = '%d.%d.%d' % version_info[:3]
if version_info.releaselevel != 'final':
    version += '-%s%s' % version_info[-2:]
    debianversion += '~adev%i' % version_info[(-1)] if RELEV == 'dev' else '~%s%i' % version_info[-2:]
    prerel = 'a' if RELEASE_LEVEL_VALUE.get(version_info[3], 0) < 10 else 'b'
    if prerel not in 'ab':
        prerel = 'a'
    strictversion += prerel + str(version_info[(-1)])
_PATTERN = None

def calc_hexversion(major=0, minor=0, micro=0, releaselevel='dev', serial=0, string=None):
    """Calculate the hexadecimal version number from the tuple version_info:

    :param major: integer
    :param minor: integer
    :param micro: integer
    :param relev: integer or string
    :param serial: integer
    :return: integer always increasing with revision numbers
    """
    global _PATTERN
    if string is not None:
        if _PATTERN is None:
            import re
            _PATTERN = re.compile('(\\d+)\\.(\\d+)\\.(\\d+)(\\w+)?$')
        result = _PATTERN.match(string)
        if result is None:
            raise ValueError("'%s' is not a valid version" % string)
        result = result.groups()
        major, minor, micro = int(result[0]), int(result[1]), int(result[2])
        releaselevel = result[3]
        if releaselevel is None:
            releaselevel = 0
        try:
            releaselevel = int(releaselevel)
        except ValueError:
            releaselevel = RELEASE_LEVEL_VALUE.get(releaselevel, 0)

        hex_version = int(serial)
        hex_version |= releaselevel * 1 << 4
        hex_version |= int(micro) * 1 << 8
        hex_version |= int(minor) * 1 << 16
        hex_version |= int(major) * 1 << 24
        return hex_version


hexversion = calc_hexversion(*version_info)
if __name__ == '__main__':
    print(version)
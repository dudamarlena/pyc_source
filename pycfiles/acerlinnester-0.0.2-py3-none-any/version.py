# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\acerim\version.py
# Compiled at: 2017-09-26 00:44:01
__doc__ = ' Keeps track of the current acerim version. Versions are specified as a\nstring of the form "X.Y.Z" (major.minor.maintenance). Versions still in\ndevelopment append \'dev0\' (e.g., "X.Y.Zdev0").\n'
_major = 0
_minor = 1
_maintenance = '1'
_extra = ''

def concatenate_version(major, minor, maintenance, extra):
    """ Construct full version string to pass to setup.py """
    _ver = [
     major, minor]
    if maintenance:
        _ver.append(maintenance)
    if extra:
        _ver.append(extra)
    return ('.').join(map(str, _ver))


__version__ = concatenate_version(_major, _minor, _maintenance, _extra)
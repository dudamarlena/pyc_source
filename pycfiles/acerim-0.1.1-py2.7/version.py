# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\acerim\version.py
# Compiled at: 2017-09-26 00:44:01
""" Keeps track of the current acerim version. Versions are specified as a
string of the form "X.Y.Z" (major.minor.maintenance). Versions still in
development append 'dev0' (e.g., "X.Y.Zdev0").
"""
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
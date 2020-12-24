# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ewheeler/dev/pygrowup/pygrowup/__init__.py
# Compiled at: 2015-06-26 06:04:19
# Size of source mod 2**32: 614 bytes
from .pygrowup import Calculator
__version_info__ = {'major': 0, 
 'minor': 8, 
 'micro': 0, 
 'releaselevel': 'beta', 
 'serial': 0}

def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ['%(major)i.%(minor)i' % __version_info__]
    if __version_info__['micro']:
        vers.append('.%(micro)i' % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(vers)


__version__ = get_version()
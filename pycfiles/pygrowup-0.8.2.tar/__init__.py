# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewheeler/dev/pygrowup/pygrowup/__init__.py
# Compiled at: 2016-03-14 07:58:27
from .pygrowup import Calculator
__version_info__ = {'major': 0, 
   'minor': 8, 
   'micro': 2, 
   'releaselevel': 'final', 
   'serial': 0}

def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ['%(major)i.%(minor)i' % __version_info__]
    if __version_info__['micro']:
        vers.append('.%(micro)i' % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ('').join(vers)


__version__ = get_version()
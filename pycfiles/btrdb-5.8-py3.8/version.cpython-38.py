# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/version.py
# Compiled at: 2020-05-13 17:11:01
# Size of source mod 2**32: 1259 bytes
"""
Maintains version and package information for deployment.
"""
__version_info__ = {'major':5, 
 'minor':8, 
 'micro':0, 
 'releaselevel':'final', 
 'serial':13}

def get_version(short=False):
    """
    Prints the version.
    """
    if not __version_info__['releaselevel'] in ('alpha', 'beta', 'final'):
        raise AssertionError
    else:
        vers = [
         '%(major)i.%(minor)i' % __version_info__]
        if __version_info__['micro']:
            vers.append('.%(micro)i' % __version_info__)
        if __version_info__['releaselevel'] != 'final':
            short or vers.append('%s%i' % (__version_info__['releaselevel'][0],
             __version_info__['serial']))
    return ''.join(vers)
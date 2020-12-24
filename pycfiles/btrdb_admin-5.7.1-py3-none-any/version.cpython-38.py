# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/version.py
# Compiled at: 2020-05-13 17:11:01
# Size of source mod 2**32: 1259 bytes
__doc__ = '\nMaintains version and package information for deployment.\n'
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
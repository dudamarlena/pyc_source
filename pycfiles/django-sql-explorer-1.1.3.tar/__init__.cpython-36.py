# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/__init__.py
# Compiled at: 2019-09-23 19:09:31
# Size of source mod 2**32: 637 bytes
__version_info__ = {'major':1,  'minor':1, 
 'micro':3, 
 'releaselevel':'final', 
 'serial':0}

def get_version(short=False):
    if not __version_info__['releaselevel'] in ('alpha', 'beta', 'final'):
        raise AssertionError
    else:
        vers = [
         '%(major)i.%(minor)i' % __version_info__]
        if __version_info__['micro']:
            vers.append('.%(micro)i' % __version_info__)
        if __version_info__['releaselevel'] != 'final':
            if not short:
                vers.append('%s%i' % (__version_info__['releaselevel'][0], __version_info__['serial']))
    return ''.join(vers)


__version__ = get_version()
default_app_config = 'explorer.apps.ExplorerAppConfig'
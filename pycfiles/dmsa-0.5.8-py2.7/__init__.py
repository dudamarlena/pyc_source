# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/__init__.py
# Compiled at: 2016-02-12 12:40:25
import os
from dmsa.makers import make_model_from_service
serial = os.environ.get('BUILD_NUM') or '0'
sha = os.environ.get('COMMIT_SHA1') or '0'
sha = sha[0:8]
__version_info__ = {'major': 0, 
   'minor': 5, 
   'micro': 8, 
   'releaselevel': 'final', 
   'serial': serial, 
   'sha': sha}

def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ['%(major)i.%(minor)i.%(micro)i' % __version_info__]
    if __version_info__['releaselevel'] != 'final' and not short:
        __version_info__['lvlchar'] = __version_info__['releaselevel'][0]
        vers.append('%(lvlchar)s%(serial)s+%(sha)s' % __version_info__)
    return ('').join(vers)


__version__ = get_version()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pypagseguro/__init__.py
# Compiled at: 2011-01-06 19:38:18
from pagseguro import Pagseguro
__author__ = 'Thaigo Avelino'
VERSION = (1, 0, 0)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    return version


__version__ = get_version()
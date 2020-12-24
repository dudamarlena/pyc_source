# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/__init__.py
# Compiled at: 2019-07-11 09:12:36
# Size of source mod 2**32: 167 bytes
__version__ = '0.3.0'
_VERBOSE = False

def set_verbose(is_verbose_on):
    global _VERBOSE
    _VERBOSE = bool(is_verbose_on)


def is_verbose():
    return bool(_VERBOSE)
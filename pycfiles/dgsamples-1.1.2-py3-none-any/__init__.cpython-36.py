# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nwlongb/dlcode/dgsamples/dgsamples/__init__.py
# Compiled at: 2018-05-30 18:47:26
# Size of source mod 2**32: 178 bytes
from . import _registerdata
allsamples = _registerdata._runit()
for _s in allsamples:
    exec(_s + '=allsamples[_s]')

from ._version import __version__
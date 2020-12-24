# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/ext/ordereddict.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 185 bytes
from sys import version_info
if version_info >= (2, 7):
    from collections import OrderedDict
else:
    from ._bundled.ordereddict import OrderedDict
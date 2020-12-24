# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/package/__init__.py
# Compiled at: 2019-01-22 13:34:55
# Size of source mod 2**32: 107 bytes
from .release import version as __version__
from .canonical import name
from .loader import load, traverse
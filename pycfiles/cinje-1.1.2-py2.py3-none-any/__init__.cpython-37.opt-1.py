# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/__init__.py
# Compiled at: 2018-11-21 11:13:57
# Size of source mod 2**32: 171 bytes
from .release import version as __version__
from .encoding import transform
from .util import stream, flatten, fragment
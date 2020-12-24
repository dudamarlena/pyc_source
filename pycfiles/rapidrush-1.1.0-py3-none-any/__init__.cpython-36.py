# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/f/develop/github/pkg-init/rapidrush/__init__.py
# Compiled at: 2019-02-03 12:58:19
# Size of source mod 2**32: 229 bytes
__all__ = [
 'rapidrush']
from rapidrush.utils.version import get_version
VERSION = (1, 1, 0, 'stable', 1)
__version__ = get_version(VERSION)
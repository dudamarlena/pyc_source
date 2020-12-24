# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/__init__.py
# Compiled at: 2019-03-10 16:25:20
# Size of source mod 2**32: 283 bytes
"""
Provides authentification and row access to Freebox using Freebox OS developer API.
Freebox API documentation : http://dev.freebox.fr/sdk/os/
"""
__version__ = '0.0.8'
__all__ = ['aiofreepybox']
from aiofreepybox.aiofreepybox import Freepybox
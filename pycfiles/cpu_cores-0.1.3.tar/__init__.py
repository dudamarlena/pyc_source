# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fab/Documents/cpu_cores/cpu_cores/__init__.py
# Compiled at: 2013-08-31 07:46:58
version_info = (0, 1, 3)
__version__ = ('.').join([ str(x) for x in version_info ])
from cpu_cores.common import CPUCoresCounter
__all__ = [
 'CPUCoresCounter']
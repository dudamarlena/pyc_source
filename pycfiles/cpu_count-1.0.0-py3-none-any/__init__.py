# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/fab/Documents/cpu_cores/cpu_cores/__init__.py
# Compiled at: 2013-08-31 07:46:58
version_info = (0, 1, 3)
__version__ = ('.').join([ str(x) for x in version_info ])
from cpu_cores.common import CPUCoresCounter
__all__ = [
 'CPUCoresCounter']
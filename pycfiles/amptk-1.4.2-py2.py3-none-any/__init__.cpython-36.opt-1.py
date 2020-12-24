# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ampoule/__init__.py
# Compiled at: 2019-05-02 00:22:24
# Size of source mod 2**32: 313 bytes
from .pool import deferToAMPProcess, pp
from .commands import Shutdown, Ping, Echo
from .child import AMPChild
from ._version import __version__ as _my_version
__version__ = _my_version.short()
__all__ = [
 'deferToAMPProcess',
 'pp',
 'Shutdown', 'Ping', 'Echo',
 'AMPChild',
 '__version__']
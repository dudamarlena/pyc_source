# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\__init__.py
# Compiled at: 2015-04-22 12:06:54
NATIVE_ASYNCIO = False
try:
    from asyncio import BaseEventLoop
    NATIVE_ASYNCIO = True
except ImportError:
    import trollius
    from trollius import From, Return

EXEC_PROCESS = 'PROCESS'
EXEC_THREAD = 'THREAD'
from .version import __author__, __version__, __email__, __description__, __status__, __license__, __url__
from .core.dsa import Dsa
from .core.instance import Instance
from .backend.user.json import JsonUserBackend
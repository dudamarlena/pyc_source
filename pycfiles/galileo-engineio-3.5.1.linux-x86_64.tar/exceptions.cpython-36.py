# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/exceptions.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 292 bytes


class EngineIOError(Exception):
    pass


class ContentTooLongError(EngineIOError):
    pass


class UnknownPacketError(EngineIOError):
    pass


class QueueEmpty(EngineIOError):
    pass


class SocketIsClosedError(EngineIOError):
    pass


class ConnectionError(EngineIOError):
    pass
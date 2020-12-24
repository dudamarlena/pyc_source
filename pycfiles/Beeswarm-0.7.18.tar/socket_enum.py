# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/socket_enum.py
# Compiled at: 2016-11-12 07:38:04
from enum import Enum

class SocketNames(Enum):
    DRONE_DATA = 'inproc://droneData'
    PROCESSED_SESSIONS = 'inproc://processedSessionPublisher'
    CONFIG_COMMANDS = 'inproc://configCommands'
    DRONE_COMMANDS = 'inproc://droneCommands'
    DATABASE_REQUESTS = 'inproc://databaseRequests'
    SERVER_COMMANDS = 'inproc://serverCommands'
    SERVER_RELAY = 'inproc://serverRelay'
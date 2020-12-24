# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/factotum/rcon.py
# Compiled at: 2017-01-20 23:06:59
# Size of source mod 2**32: 513 bytes
from factoirc.rcon import RconConnection
import asyncio, sys

def rconCmd(cmd):
    host = 'localhost'
    port = 27015
    try:
        with open('/tmp/factorioRcon', 'r') as (phraseFile):
            phrase = phraseFile.readline().strip()
            cmd = ' '.join(cmd)
            loop = asyncio.get_event_loop()
            conn = RconConnection(host, port, phrase)
            resp = loop.run_until_complete(conn.exec_command(cmd))
            print(resp, end='')
    except FileNotFoundError:
        print('Cannot find the rcon password. Is the server running?')
        sys.exit(1)
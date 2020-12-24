# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/db/conn.py
# Compiled at: 2020-04-03 01:07:15
# Size of source mod 2**32: 265 bytes
from ssdb import Client as DbClient
from ..aa import get_env

def conn_db(host: str=None, port: int=None) -> DbClient:
    if host or port:
        return DbClient(host, port)
    env = get_env()
    return DbClient(env.db_host, env.db_port)
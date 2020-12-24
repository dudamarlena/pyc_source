# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/server/db.py
# Compiled at: 2016-03-02 18:41:19
# Size of source mod 2**32: 1025 bytes
import asyncio, logging
from typing import Dict, Any
import aiopg.sa
log = logging.getLogger(__name__)

def setup_database(loop: asyncio.AbstractEventLoop, config: Dict[(str, Any)]) -> aiopg.sa.Engine:
    """ Configure and return sqlalchemy's Engine instance with a
    built-in connection pool.
    """
    log.debug('Establishing connection with PostgreSQL...')
    dbconf = config['postgresql']
    dsn = 'dbname={dbname} user={user} password={password} host={host} port={port}'.format(user=dbconf['user'], password=dbconf['password'], host=dbconf['host'], port=dbconf['port'], dbname=dbconf['dbname'])
    engine = await aiopg.sa.create_engine(dsn=dsn, minsize=dbconf['min_connections'], maxsize=dbconf['max_connections'], loop=loop, echo=config['debug'])
    return engine
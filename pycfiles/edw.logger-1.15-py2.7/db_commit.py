# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/events/db_commit.py
# Compiled at: 2018-04-03 08:40:41
import json, logging, transaction
from datetime import datetime
from ZODB.Connection import Connection
from edw.logger.util import get_request_data
from edw.logger.decorators import log_errors
from edw.logger.config import logger
from edw.logger.config import LOG_DB

def __after_conn_close(request_data):

    @log_errors('Cannot log transaction commit.')
    def on_close():
        url = request_data['url']
        logger.info(json.dumps({'IP': request_data['ip'], 
           'User': request_data['user'], 
           'Date': datetime.now().isoformat(), 
           'URL': url, 
           'Action': request_data['action'], 
           'Type': 'Commit', 
           'LoggerName': logger.name}))

    return on_close


@log_errors('Cannot log transaction commit.')
def handler_commit(event):
    """ Handle ZPublisher.pubevents.PubBeforeCommit.
        This is the only event where we can intercept a
        transaction before it gets committed. Also the only
        event where hooks can be placed and ensure they are
        only executed after a true DB commit.
    """
    if not LOG_DB:
        return
    txn = transaction.get()
    request = event.request
    request_data = get_request_data(request)
    for conn in (c for c in txn._resources if isinstance(c, Connection)):
        conn.onCloseCallback(__after_conn_close(request_data))
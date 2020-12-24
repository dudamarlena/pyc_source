# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_postgresql_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.postgresql_log import PostgreSQLLog
from insights.tests import context_wrap
POSTGRESQL_LOG = '\nLOG:  unexpected EOF on client connection\nLOG:  received fast shutdown request\nLOG:  aborting any active transactions\nFATAL:  terminating connection due to administrator command\nFATAL:  terminating connection due to administrator command\nLOG:  autovacuum launcher shutting down\nFATAL:  terminating connection due to administrator command\nLOG:  shutting down\nLOG:  database system is shut down\nLOG:  database system was shut down at 2015-11-10 18:36:41 EST\nLOG:  database system is ready to accept connections\nLOG:  autovacuum launcher started\n'

def test_postgresql_log():
    log = PostgreSQLLog(context_wrap(POSTGRESQL_LOG))
    assert 'FATAL:  terminating connection' in log
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mariadb_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.mariadb_log import MariaDBLog
from insights.tests import context_wrap
from datetime import datetime
MARIADB_LOG = '\n161109  9:25:42 [Warning] SSL error: SSL_CTX_set_default_verify_paths failed\n161109  9:25:42 [Note] WSREP: Service disconnected.\n161109  9:25:43 [Note] WSREP: Some threads may fail to exit.\n161109 14:28:24 InnoDB: Initializing buffer pool, size = 128.0M\n161109 14:28:24 InnoDB: Completed initialization of buffer pool\n'

def test_mariadb_log():
    log = MariaDBLog(context_wrap(MARIADB_LOG))
    assert len(log.get('[Warning]')) == 1
    assert len(log.get('[Note]')) == 2
    assert 'SSL_CTX_set_default_verify_paths' in log
    assert len(list(log.get_after(datetime(2016, 11, 9, 14, 0, 0)))) == 2
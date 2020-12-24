# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mysql_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.mysql_log import MysqlLog
from insights.tests import context_wrap
MYSQL_LOG = "\n2018-03-13T06:37:37.268209Z 0 [Warning] Changed limits: max_open_files: 1024 (requested 5000)\n2018-03-13T06:37:37.268417Z 0 [Warning] Changed limits: table_open_cache: 431 (requested 2000)\n2018-03-13T06:37:37.268549Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation fo\nr more details).\n2018-03-13T06:37:39.651387Z 0 [Warning] InnoDB: New log files created, LSN=45790\n2018-03-13T06:37:39.719166Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.\n2018-03-13T06:37:39.784406Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 0\n698a7d6-2689-11e8-8944-0800274ac5ef.\n2018-03-13T06:37:39.789636Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.\n2018-03-13T06:37:40.498084Z 0 [Warning] CA certificate ca.pem is self signed.\n2018-03-13T06:37:41.080591Z 1 [Warning] root@localhost is created with an empty password ! Please consider switching off the --initialize-insecure option.\nmd5_dgst.c(80): OpenSSL internal error, assertion failed: Digest MD5 forbidden in FIPS mode!\n06:37:41 UTC - mysqld got signal 6 ;\n2018-03-13T07:43:31.450772Z 0 [Note] Event Scheduler: Loaded 0 events\n2018-03-13T07:43:31.450988Z 0 [Note] /opt/rh/rh-mysql57/root/usr/libexec/mysqld: ready for connections.\nVersion: '5.7.16'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  MySQL Community Server (GPL)\nmd5_dgst.c(80): OpenSSL internal error, assertion failed: Digest MD5 forbidden in FIPS mode!\n07:46:19 UTC - mysqld got signal 6 ;\n"

def test_mysql_log():
    log = MysqlLog(context_wrap(MYSQL_LOG))
    assert len(log.get('[Warning]')) == 9
    assert len(log.get('[Note]')) == 2
    assert 'ready for connections' in log
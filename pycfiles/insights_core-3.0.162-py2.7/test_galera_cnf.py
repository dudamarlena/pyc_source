# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_galera_cnf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.galera_cnf import GaleraCnf
from insights.tests import context_wrap
GALERA_CNF = '\n[client]\nport = 3306\nsocket = /var/lib/mysql/mysql.sock\n\n[isamchk]\nkey_buffer_size = 16M\n\n[mysqld]\nbasedir = /usr\nbinlog_format = ROW\ndatadir = /var/lib/mysql\ndefault-storage-engine = innodb\nexpire_logs_days = 10\ninnodb_autoinc_lock_mode = 2\ninnodb_locks_unsafe_for_binlog = 1\nkey_buffer_size = 16M\nlog-error = /var/log/mariadb/mariadb.log\nmax_allowed_packet = 16M\nmax_binlog_size = 100M\nmax_connections = 8192\nwsrep_max_ws_rows = 131072\nwsrep_max_ws_size = 1073741824\n\n[mysqld_safe]\nlog-error = /var/log/mariadb/mariadb.log\nnice = 0\nsocket = /var/lib/mysql/mysql.sock\n\n[mysqldump]\nmax_allowed_packet = 16M\nquick\nquote-names\n'

def test_galera_cnf():
    cnf = GaleraCnf(context_wrap(GALERA_CNF))
    assert cnf is not None
    assert cnf.get('client', 'port') == '3306'
    assert cnf.get('isamchk', 'key_buffer_size') == '16M'
    assert cnf.get('mysqld', 'max_connections') == '8192'
    assert 'not_there' not in cnf
    assert cnf.get('mysqldump', 'quick') is None
    return
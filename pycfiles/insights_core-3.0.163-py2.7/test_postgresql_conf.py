# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_postgresql_conf.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.tests import context_wrap
from insights.parsers.postgresql_conf import PostgreSQLConf
postgresql_conf_cnt = ('\n\n# -----------------------------\n# PostgreSQL configuration file\n# -----------------------------\n#\n# This file consists of lines of the form:\n#\n#   name = value\n#\n# (The "=" is optional.)  Whitespace may be used.  Comments are introduced with\n# "#" anywhere on a line.  The complete list of parameter names and allowed\n# values can be found in the PostgreSQL documentation.\n#\n# The commented-out settings shown in this file represent the default values.\n# Re-commenting a setting is NOT sufficient to revert it to the default value;\n# you need to reload the server.\n#\n# This file is read on server startup and when the server receives a SIGHUP\n# signal.  If you edit the file on a running system, you have to SIGHUP the\n# server for the changes to take effect, or use "pg_ctl reload".  Some\n# parameters, which are marked below, require a server shutdown and restart to\n# take effect.\n#\n# Any parameter can also be given as a command-line option to the server, e.g.,\n# "postgres -c log_connections=on".  Some parameters can be changed at run time\n# with the "SET" SQL command.\n#\n# Memory units:  kB = kilobytes        Time units:  ms  = milliseconds\n#                MB = megabytes                     s   = seconds\n#                GB = gigabytes                     min = minutes\n#                                                   h   = hours\n#                                                   d   = days\n\n\n#------------------------------------------------------------------------------\n# FILE LOCATIONS\n#------------------------------------------------------------------------------\n\n# The default values of these variables are driven from the -D command-line\n# option or PGDATA environment variable, represented here as ConfigDir.\n\n#data_directory = \'ConfigDir\'\t\t# use data in another directory\n#hba_file = \'ConfigDir/pg_hba.conf\'\t# host-based authentication file\n#ident_file = \'ConfigDir/pg_ident.conf\'\t# ident configuration file\n\n# If external_pid_file is not explicitly set, no extra PID file is written.\n#external_pid_file = \'(none)\'\t\t# write an extra PID file\n\n\n#------------------------------------------------------------------------------\n# CONNECTIONS AND AUTHENTICATION\n#------------------------------------------------------------------------------\n\n# - Connection Settings -\n\n#listen_addresses = \'localhost\'\t\t# what IP address(es) to listen on;\n#port = 5432\t\t\t\t# (change requires restart)\n### next line has been commented out by spacewalk-setup-postgresql ###\n##max_connections = 100\t\t\t# (change requires restart)\n# Note:  Increasing max_connections costs ~400 bytes of shared memory per\n# connection slot, plus lock space (see max_locks_per_transaction).\n#superuser_reserved_connections = 3\t# (change requires restart)\n#unix_socket_directory = \'\'\t\t# (change requires restart)\n#unix_socket_group = \'\'\t\t\t# (change requires restart)\n#unix_socket_permissions = 0777\t\t# begin with 0 to use octal notation\n#bonjour_name = \'\'\t\t\t# defaults to the computer name\n\n# - Security and Authentication -\n\n#authentication_timeout = 1min\t\t# 1s-600s\n#ssl = off\t\t\t\t# (change requires restart)\n#ssl_ciphers = \'ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH\'\t# allowed SSL ciphers\n#ssl_renegotiation_limit = 512MB\t# amount of data between renegotiations\n#password_encryption = on\n#db_user_namespace = off\n\n# Kerberos and GSSAPI\n#krb_server_keyfile = \'\'\n#krb_srvname = \'postgres\'\t\t# (Kerberos only)\n#krb_caseins_users = off\n\n# - TCP Keepalives -\n# see "man 7 tcp" for details\n\n#tcp_keepalives_idle = 0\t\t# TCP_KEEPIDLE, in seconds;\n#tcp_keepalives_interval = 0\t\t# TCP_KEEPINTVL, in seconds;\n#tcp_keepalives_count = 0\t\t# TCP_KEEPCNT;\n\n#------------------------------------------------------------------------------\n# RESOURCE USAGE (except WAL)\n#------------------------------------------------------------------------------\n\n# - Memory -\n\n### next line has been commented out by spacewalk-setup-postgresql ###\n##shared_buffers = 32MB\t\t\t# min 128kB\n#temp_buffers = 8MB\t\t\t# min 800kB\n#max_prepared_transactions = 0\t\t# zero disables the feature\n# Note:  Increasing max_prepared_transactions costs ~600 bytes of shared memory\n# per transaction slot, plus lock space (see max_locks_per_transaction).\n# It is not advisable to set max_prepared_transactions nonzero unless you\n# actively intend to use prepared transactions.\n#work_mem = 1MB\t\t\t\t# min 64kB\n#maintenance_work_mem = 16MB\t\t# min 1MB\n#max_stack_depth = 2MB\t\t\t# min 100kB\n\n# - Kernel Resource Usage -\n\n#max_files_per_process = 1000\t\t# min 25\n#shared_preload_libraries = \'\'\t\t# (change requires restart)\n\n# - Cost-Based Vacuum Delay -\n\n#vacuum_cost_delay = 0ms\t\t# 0-100 milliseconds\n#vacuum_cost_page_hit = 1\t\t# 0-10000 credits\n#vacuum_cost_page_miss = 10\t\t# 0-10000 credits\n#vacuum_cost_page_dirty = 20\t\t# 0-10000 credits\n#vacuum_cost_limit = 200\t\t# 1-10000 credits\n\n# - Background Writer -\n\n#bgwriter_delay = 200ms\t\t\t# 10-10000ms between rounds\n#bgwriter_lru_maxpages = 100\t\t# 0-1000 max buffers written/round\n#bgwriter_lru_multiplier = 2.0\t\t# 0-10.0 multipler on buffers scanned/round\n\n# - Asynchronous Behavior -\n\n#effective_io_concurrency = 1\t\t# 1-1000. 0 disables prefetching\n\n# These are only used if logging_collector is on:\nlog_directory = \'pg_log\'\t\t# directory where log files are written,\nlog_filename = \'postgresql-%a.log\'\t# log file name pattern,\nlog_truncate_on_rotation = on\t\t# If on, an existing log file of the\ncheckpoint_completion_target = 0.7\ncheckpoint_segments = 8\neffective_cache_size = 1152MB\nlog_line_prefix = \'%m \'\nmaintenance_work_mem = 96MB\nmax_connections = 600\nshared_buffers = 384MB\nwal_buffers = 4MB\nwork_mem = 2560kB\n\npassword_encryption on\ndb_user_namespace = off\n\nbgwriter_delay = 200ms\t\t\t# 10-10000ms between rounds\ncheckpoint_timeout = 5min\ntcp_keepalives_interval 300\n\nmax_stack_depth = 2048576       # Test of as_memory_bytes with string of digits\n\ntest_strange_quoting \'\'\'strange quoting\\\'\'\n').strip()

def test_postgresql_conf():
    result = PostgreSQLConf(context_wrap(postgresql_conf_cnt))
    assert result.get('checkpoint_segments') == '8'
    assert result.get('log_filename') == 'postgresql-%a.log'
    assert result.get('log_line_prefix') == '%m '
    assert result.get('password_encryption') == 'on'
    assert result.get('test_strange_quoting') == "'strange quoting'"
    assert result.get(None) is None
    assert result.get('') is None
    assert 'listen_addresses' not in result
    assert result.get('listen_addresses', 'localhost') == 'localhost'
    return


def test_postgresql_conf_conversions():
    result = PostgreSQLConf(context_wrap(postgresql_conf_cnt))
    assert result.as_duration('bgwriter_delay') == 0.2
    assert result.as_duration('checkpoint_timeout') == 300
    assert result.as_duration('tcp_keepalives_interval') == 300
    assert result.as_duration(None) is None
    assert 'vacuum_cost_delay' not in result
    assert result.as_duration('vacuum_cost_delay', '200ms') == 0.2
    assert result.as_duration('tcp_keepalives_idle', '0') == 0
    assert result.as_duration('tcp_keepalives_idle', 0) == 0
    assert result.as_boolean('password_encryption')
    assert not result.as_boolean('db_user_namespace')
    assert result.as_boolean(None) is None
    assert result.as_boolean('no_such_property', True)
    assert 'krb_caseins_users' not in result
    assert not result.as_boolean('krb_caseins_users', 'no')
    assert result.as_memory_bytes('work_mem') == 2621440
    assert result.as_memory_bytes('wal_buffers') == 4194304
    assert result.as_memory_bytes('max_stack_depth') == 2048576
    assert result.as_memory_bytes(None) is None
    assert 'temp_buffers' not in result
    assert result.as_memory_bytes('temp_buffers', '8MB') == 8388608
    assert result.as_memory_bytes('temp_buffers', '8388608') == 8388608
    assert result.as_memory_bytes('temp_buffers', 8388608) == 8388608
    return


def test_postgresql_conf_conversion_errors():
    result = PostgreSQLConf(context_wrap(postgresql_conf_cnt))
    with pytest.raises(ValueError):
        assert result.as_duration('log_filename')
    with pytest.raises(ValueError):
        assert result.as_duration('db_user_namespace')
    with pytest.raises(ValueError):
        assert result.as_boolean('log_directory')
    with pytest.raises(ValueError):
        assert result.as_boolean('checkpoint_segments')
    with pytest.raises(ValueError):
        assert result.as_memory_bytes('log_line_prefix')
    with pytest.raises(ValueError):
        assert result.as_memory_bytes('checkpoint_timeout')
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdcheck/cnf.py
# Compiled at: 2020-02-08 12:06:07
# Size of source mod 2**32: 2545 bytes
"""
slapdcheck.cnf - Configuration constants
"""
import sys, os, ldap0
STATE_FILENAME = 'slapd_checkmk.state'
CHECK_RESULT_OK = 0
CHECK_RESULT_WARNING = 1
CHECK_RESULT_ERROR = 2
CHECK_RESULT_UNKNOWN = 3
CHECK_RESULT_NOOP_SRCH_UNAVAILABLE = CHECK_RESULT_OK
LDAP_TIMEOUT = 4.0
SLAPD_SOCK_TIMEOUT = 2.0
NOOP_SEARCH_TIMEOUT = 6.0
MINIMUM_ENTRY_COUNT = 20
SYNCREPL_TIMEDELTA_WARN = 5.0
SYNCREPL_TIMEDELTA_CRIT = 300.0
SYNCREPL_HYSTERESIS_WARN = 0.0
SYNCREPL_HYSTERESIS_CRIT = 10.0
SYNCREPL_PROVIDER_ERROR_PERCENTAGE = 50.0
OPS_WAITING_WARN = 30
OPS_WAITING_CRIT = 60
CONNECTIONS_WARN_LOWER = 3
CONNECTIONS_WARN_PERCENTAGE = 80.0
THREADS_ACTIVE_WARN_LOWER = 1
THREADS_ACTIVE_WARN_UPPER = 6
THREADS_PENDING_WARN = 5

class NoneException(BaseException):
    __doc__ = '\n    A dummy exception class used for disabling exception handling\n    '


CATCH_ALL_EXC = (
 Exception, ldap0.LDAPError)
CERT_ERROR_DAYS = 10
CERT_WARN_DAYS = 50
LDAP0_TRACE_LEVEL = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))
ldap0._trace_level = LDAP0_TRACE_LEVEL
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_httpd_V.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import httpd_V
from insights.parsers import SkipException
from insights.parsers.httpd_V import HttpdV
from insights.tests import context_wrap
import pytest, doctest
HTTPD_V_22 = ('\nServer version: Apache/2.2.15 (Unix)\nServer built:   Feb  4 2016 02:44:09\nServer\'s Module Magic Number: 20051115:25\nServer loaded:  APR 1.3.9, APR-Util 1.3.9\nCompiled using: APR 1.3.9, APR-Util 1.3.9\nArchitecture:   64-bit\nServer MPM:     Prefork\n  threaded:     no\n    forked:     yes (variable process count)\nServer compiled with....\n -D APACHE_MPM_DIR="server/mpm/prefork"\n -D APR_HAS_SENDFILE\n -D APR_HAS_MMAP\n -D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)\n -D APR_USE_SYSVSEM_SERIALIZE\n -D APR_USE_PTHREAD_SERIALIZE\n -D SINGLE_LISTEN_UNSERIALIZED_ACCEPT\n -D APR_HAS_OTHER_CHILD\n -D AP_HAVE_RELIABLE_PIPED_LOGS\n -D DYNAMIC_MODULE_LIMIT=128\n -D HTTPD_ROOT="/etc/httpd"\n -D SUEXEC_BIN="/usr/sbin/suexec"\n -D DEFAULT_PIDLOG="run/httpd.pid"\n -D DEFAULT_SCOREBOARD="logs/apache_runtime_status"\n -D DEFAULT_LOCKFILE="logs/accept.lock"\n -D DEFAULT_ERRORLOG="logs/error_log"\n -D AP_TYPES_CONFIG_FILE="conf/mime.types"\n -D SERVER_CONFIG_FILE="conf/httpd.conf"\n').strip()
HTTPD_V_24 = ('\nServer version: Apache/2.4.6 (Red Hat Enterprise Linux)\nServer built:   Aug  3 2016 08:33:27\nServer\'s Module Magic Number: 20120211:24\nServer loaded:  APR 1.4.8, APR-UTIL 1.5.2\nCompiled using: APR 1.4.8, APR-UTIL 1.5.2\nArchitecture:   64-bit\nServer MPM:     Worker\n  threaded:     no\n    forked:     yes (variable process count)\nServer compiled with....\n -D APR_HAS_SENDFILE\n -D APR_HAS_MMAP\n -D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)\n -D APR_USE_SYSVSEM_SERIALIZE\n -D APR_USE_PTHREAD_SERIALIZE\n -D SINGLE_LISTEN_UNSERIALIZED_ACCEPT\n -D APR_HAS_OTHER_CHILD\n -D AP_HAVE_RELIABLE_PIPED_LOGS\n -D DYNAMIC_MODULE_LIMIT=256\n -D HTTPD_ROOT="/etc/httpd"\n -D SUEXEC_BIN="/usr/sbin/suexec"\n -D DEFAULT_PIDLOG="/run/httpd/httpd.pid"\n -D DEFAULT_SCOREBOARD="logs/apache_runtime_status"\n -D DEFAULT_ERRORLOG="logs/error_log"\n -D AP_TYPES_CONFIG_FILE="conf/mime.types"\n -D SERVER_CONFIG_FILE="conf/httpd.conf"\n').strip()
HTTPDV_DOC = ('\nServer version: Apache/2.2.6 (Red Hat Enterprise Linux)\nServer\'s Module Magic Number: 20120211:24\nCompiled using: APR 1.4.8, APR-UTIL 1.5.2\nArchitecture:   64-bit\nServer MPM:     Prefork\nServer compiled with....\n-D APR_HAS_SENDFILE\n-D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)\n-D AP_TYPES_CONFIG_FILE="conf/mime.types"\n-D SERVER_CONFIG_FILE="conf/httpd.conf"\n').strip()

def test_httpd_V():
    result = HttpdV(context_wrap(HTTPD_V_22, path='/usr/sbin/httpd_-V'))
    assert result['Server MPM'] == 'prefork'
    assert result['Server version'] == 'apache/2.2.15 (unix)'
    assert result['forked'] == 'yes (variable process count)'
    assert 'APR_HAVE_IPV6' in result['Server compiled with']
    assert result['Server compiled with']['APR_HAS_MMAP'] is True
    assert result['Server compiled with']['APR_HAVE_IPV6'] == 'IPv4-mapped addresses enabled'
    assert result['Server compiled with']['DEFAULT_PIDLOG'] == 'run/httpd.pid'
    assert result.httpd_command == '/usr/sbin/httpd'
    assert result.mpm == 'prefork'
    assert result.version == 'apache/2.2.15 (unix)'
    result = HttpdV(context_wrap(HTTPD_V_24, path='/usr/sbin/httpd.worker_-V'))
    assert result['Server MPM'] == 'worker'
    assert result['Server version'] == 'apache/2.4.6 (red hat enterprise linux)'
    assert result['forked'] == 'yes (variable process count)'
    assert 'APR_HAVE_IPV6' in result['Server compiled with']
    assert result['Server compiled with']['APR_HAS_MMAP'] is True
    assert result['Server compiled with']['APR_HAVE_IPV6'] == 'IPv4-mapped addresses enabled'
    assert result['Server compiled with']['DEFAULT_PIDLOG'] == '/run/httpd/httpd.pid'
    assert result.httpd_command == '/usr/sbin/httpd.worker'
    assert result.mpm == 'worker'
    assert result.version == 'apache/2.4.6 (red hat enterprise linux)'


def test_httpd_V_exp():
    with pytest.raises(SkipException) as (sc):
        HttpdV(context_wrap(''))
    assert 'Input content is empty' in str(sc)
    with pytest.raises(SkipException) as (sc):
        HttpdV(context_wrap('TEST'))
    assert 'Input content is not empty but there is no useful parsed data.' in str(sc)


def test_httpd_V_doc():
    env = {'hv': HttpdV(context_wrap(HTTPDV_DOC))}
    failed, total = doctest.testmod(httpd_V, globs=env)
    assert failed == 0
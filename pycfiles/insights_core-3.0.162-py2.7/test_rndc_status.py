# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rndc_status.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import rndc_status, ParseException, SkipException
from insights.parsers.rndc_status import RndcStatus
from insights.tests import context_wrap
RNDC_STATUS = ('\nversion: BIND 9.11.4-P2-RedHat-9.11.4-9.P2.el7 (Extended Support Version) <id:7107deb>\nrunning on rhel7: Linux x86_64 3.10.0-957.10.1.el7.x86_64 #1 SMP Thu Feb 7 07:12:53 UTC 2019\nboot time: Mon, 26 Aug 2019 02:17:03 GMT\nlast configured: Mon, 26 Aug 2019 02:17:03 GMT\nconfiguration file: /etc/named.conf\nCPUs found: 4\nworker threads: 4\nUDP listeners per interface: 3\nnumber of zones: 103 (97 automatic)\ndebug level: 0\nxfers running: 0\nxfers deferred: 0\nsoa queries in progress: 0\nquery logging is OFF\nrecursive clients: 0/900/1000\ntcp clients: 1/150\nserver is up and running\n').strip()
RNDC_STATUS_INVALID = ('\ninvalid\ninvalid\ninvalid\n').strip()
RNDC_STATUS_EMPTY = ('\n').strip()

def test_rndc_status():
    rndc_status = RndcStatus(context_wrap(RNDC_STATUS))
    assert rndc_status['boot time'] == 'Mon, 26 Aug 2019 02:17:03 GMT'
    assert rndc_status['server'] == 'up and running'


def test_invalid():
    with pytest.raises(ParseException) as (e):
        RndcStatus(context_wrap(RNDC_STATUS_INVALID))
    assert 'invalid' in str(e)


def test_empty():
    with pytest.raises(SkipException) as (e):
        RndcStatus(context_wrap(RNDC_STATUS_EMPTY))
    assert 'Empty content' in str(e)


def test_rndc_status_doc_examples():
    env = {'rndc_status': RndcStatus(context_wrap(RNDC_STATUS))}
    failed, total = doctest.testmod(rndc_status, globs=env)
    assert failed == 0
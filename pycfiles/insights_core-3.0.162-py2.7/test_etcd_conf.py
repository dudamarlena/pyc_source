# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_etcd_conf.py
# Compiled at: 2019-11-14 13:57:46
import pytest, doctest
from insights.parsers import etcd_conf, SkipException
from insights.tests import context_wrap
from insights.parsers.etcd_conf import EtcdConf
ETCD_CONF = ('\n\n[member]\nETCD_NAME=f05-h19-000-1029p.rdu2.scalelab.redhat.com\nETCD_LISTEN_PEER_URLS=https://10.1.40.235:2380\nETCD_DATA_DIR=/var/lib/etcd/\n#ETCD_WAL_DIR=\nETCD_SNAPSHOT_COUNT=10000\nETCD_HEARTBEAT_INTERVAL=500\n\n[auth]\nETCD_AUTH_TOKEN=simple\n\n').strip()

def test_etcd_conf_empty():
    with pytest.raises(SkipException):
        assert etcd_conf.EtcdConf(context_wrap('')) is None
    return


def test_etcd_conf():
    conf = EtcdConf(context_wrap(ETCD_CONF))
    assert conf.has_option('member', 'ETCD_HEARTBEAT_INTERVAL') is True


def test_etcd_conf_documentation():
    failed_count, tests = doctest.testmod(etcd_conf, globs={'conf': EtcdConf(context_wrap(ETCD_CONF))})
    assert failed_count == 0
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ceph_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import ceph_conf, SkipException
from insights.tests import context_wrap
CEPH_CONF = '\n[global]\nosd_pool_default_pgp_num = 128\nauth_service_required = cephx\nmon_initial_members = controller1-az1,controller1-az2,controller1-az3\nfsid = a4c3-11e8-99c5-5254003f2830-ea8796d6\ncluster_network = 10.xx.xx.xx/23\nauth_supported = cephx\nauth_cluster_required = cephx\nmon_host = 10.xx.xx.xx,xx.xx.xx.xx,10.xx.xx.xx\nauth_client_required = cephx\nosd_pool_default_size = 3\nosd_pool_default_pg_num = 128\nms_bind_ipv6 = false\npublic_network = 10.xx.xx.xx/23\n\n[osd]\nosd_journal_size = 81920\n\n[mon.controller1-az2]\npublic_addr = 10.xx.xx.xx\n\n[client.radosgw.gateway]\nuser = apache\nrgw_frontends = civetweb port=10.xx.xx.xx:8080\nlog_file = /var/log/ceph/radosgw.log\nhost = controller1-az2\nkeyring = /etc/ceph/ceph.client.radosgw.gateway.keyring\nrgw_keystone_implicit_tenants = true\nrgw_keystone_token_cache_size = 500\nrgw_keystone_url = http://10.xx.xx.xx:35357\nrgw_s3_auth_use_keystone = true\nrgw_keystone_admin_467fE = Xqzta6dYhPHGHGEFaGnctoken\nrgw_keystone_accepted_roles = admin,_member_,Member\nrgw_swift_account_in_url = true\n'

def test_ceph_conf_empty():
    with pytest.raises(SkipException):
        assert ceph_conf.CephConf(context_wrap('')) is None
    return


def test_ceph_conf():
    conf = ceph_conf.CephConf(context_wrap(CEPH_CONF))
    assert list(conf.sections()) == ['global',
     'osd',
     'mon.controller1-az2',
     'client.radosgw.gateway']
    assert conf.has_option('osd', 'osd_journal_size') is True
    assert conf.getboolean('client.radosgw.gateway', 'rgw_swift_account_in_url') is True
    assert conf.get('client.radosgw.gateway', 'rgw_swift_account_in_url') == 'true'
    assert conf.get('client.radosgw.gateway', 'user') == 'apache'
    assert conf.get('client.radosgw.gateway', 'log_file') == '/var/log/ceph/radosgw.log'


def test_ceph_conf_documentation():
    failed_count, tests = doctest.testmod(ceph_conf, globs={'conf': ceph_conf.CephConf(context_wrap(CEPH_CONF))})
    assert failed_count == 0
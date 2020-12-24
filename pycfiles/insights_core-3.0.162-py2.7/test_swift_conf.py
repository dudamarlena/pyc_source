# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_swift_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.tests import context_wrap
from insights.parsers import swift_conf
proxy_server_conf = '\n[DEFAULT]\nbind_port = 8080\nbind_ip = 172.20.15.20\nworkers = 0\nuser = swift\nlog_name = proxy-server\nlog_facility = LOG_LOCAL1\nlog_level = INFO\nlog_headers = False\nlog_address = /dev/log\n[pipeline:main]\npipeline = catch_errors healthcheck proxy-logging cache ratelimit bulk tempurl formpost authtoken keystone staticweb versioned_writes ceilometer proxy-logging proxy-server\n[app:proxy-server]\nuse = egg:swift#proxy\nset log_name = proxy-server\nset log_facility = LOG_LOCAL1\nset log_level = INFO\nset log_address = /dev/log\nlog_handoffs = true\nallow_account_management = true\naccount_autocreate = true\nnode_timeout = 60\n[filter:catch_errors]\nuse = egg:swift#catch_errors\n[filter:bulk]\nuse = egg:swift#bulk\nmax_containers_per_extraction = 10000\nmax_failed_extractions = 1000\nmax_deletes_per_request = 10000\nyield_frequency = 60\n[filter:tempurl]\nuse = egg:swift#tempurl\n[filter:formpost]\nuse = egg:swift#formpost\n[filter:authtoken]\nlog_name = swift\nsigning_dir = /var/cache/swift\npaste.filter_factory = keystonemiddleware.auth_token:filter_factory\nauth_uri = http://172.20.3.28:5000/v2.0\nauth_url = http://172.20.4.106:35357\nauth_plugin = password\nproject_domain_id = default\nuser_domain_id = default\nproject_name = service\nusername = swift\ndelay_auth_decision = 1\ncache = swift.cache\ninclude_service_catalog = false\n[filter:keystone]\nuse = egg:swift#keystoneauth\noperator_roles = admin, swiftoperator, ResellerAdmin\nreseller_prefix = AUTH_\n[filter:staticweb]\nuse = egg:swift#staticweb\nurl_base = https://10.75.13.138:13808\n[filter:versioned_writes]\nuse = egg:swift#versioned_writes\nallow_versioned_writes = true\n[filter:ceilometer]\npaste.filter_factory = ceilometermiddleware.swift:filter_factory\nurl = rabbit://guest:J8F22AqWpXqCJyv3mQKeRQszG@172.20.3.20:5672,guest:J8F22AqWpXqCJyv3mQKeRQszG@172.20.3.31:5672,guest:J8F22AqWpXqCJyv3mQKeRQszG@172.20.3.22:5672//\nurl_test =\n'
object_expirer = '\n[DEFAULT]\n[object-expirer]\n# auto_create_account_prefix = .\nauto_create_account_prefix = .\nprocess=0\nconcurrency=1\nrecon_cache_path=/var/cache/swift\ninterval=300\nreclaim_age=604800\nreport_interval=300\nprocesses=0\nexpiring_objects_account_name=expiring_objects\n[pipeline:main]\npipeline = catch_errors cache proxy-server\n[app:proxy-server]\nuse = egg:swift#proxy\n[filter:cache]\nuse = egg:swift#memcache\nmemcache_servers = 172.16.64.60:11211\n[filter:catch_errors]\nuse = egg:swift#catch_errors\n'
SWIFT_CONF = '\n[swift-hash]\n# random unique strings that can never change (DO NOT LOSE)\n# Use only printable chars (python -c "import string; print(string.printable)")\nswift_hash_path_prefix = changeme\nswift_hash_path_suffix = changeme\n\n[storage-policy:0]\nname = gold\npolicy_type = replication\ndefault = yes\n\n[storage-policy:1]\nname = silver\npolicy_type = replication\n\n[storage-policy:2]\nname = ec42\npolicy_type = erasure_coding\nec_type = liberasurecode_rs_vand\nec_num_data_fragments = 4\nec_num_parity_fragments = 2\n'

def test_proxy_server_conf():
    result = swift_conf.SwiftProxyServerConf(context_wrap(proxy_server_conf))
    assert 'filter:ceilometer' in result
    assert 'filter:staticweb' in result
    assert result.items('filter:ceilometer').get('url_test') == ''
    assert result.getint('DEFAULT', 'bind_port') == 8080


def test_object_expirer_conf():
    result = swift_conf.SwiftObjectExpirerConf(context_wrap(object_expirer))
    assert 'filter:cache' in result
    assert 'object-expirer' in result
    assert result.get('filter:cache', 'memcache_servers') == '172.16.64.60:11211'
    assert result.getint('object-expirer', 'report_interval') == 300


def test_swift_conf():
    conf = swift_conf.SwiftConf(context_wrap(SWIFT_CONF))
    assert 'swift-hash' in conf.sections()
    assert conf.has_option('storage-policy:2', 'policy_type') is True
    assert conf.get('storage-policy:2', 'policy_type') == 'erasure_coding'
    assert conf.get('storage-policy:2', 'ec_type') == 'liberasurecode_rs_vand'


def test_swift_conf_documentation():
    failed_count, tests = doctest.testmod(swift_conf, globs={'swift_conf': swift_conf.SwiftConf(context_wrap(SWIFT_CONF)), 'object_expirer_conf': swift_conf.SwiftObjectExpirerConf(context_wrap(object_expirer)), 
       'proxy_server_conf': swift_conf.SwiftProxyServerConf(context_wrap(proxy_server_conf))})
    assert failed_count == 0
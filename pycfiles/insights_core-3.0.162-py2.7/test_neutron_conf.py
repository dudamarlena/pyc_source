# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.neutron_conf import NeutronConf
from insights.tests import context_wrap
NEUTRON_CONF = '\n[DEFAULT]\n# debug = False\ndebug = False\n# verbose = True\nverbose = False\ncore_plugin =neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2\n\n[quotas]\ndefault_quota = -1\nquota_network = 10\n[agent]\nreport_interval = 60\n\n[keystone_authtoken]\nauth_host = ost-controller-lb-del.om-l.dsn.inet\nauth_port = 35357\n[database]\nconnection = mysql://neutron:dSNneutron01@ost-mysql.om-l.dsn.inet/neutron?ssl_ca=/etc/pki/CA/certs/ca.crt\n[service_providers]\nservice_provider = LOADBALANCER:Haproxy:neutron.services.loadbalancer.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default\n'

def test_neutron_conf():
    nconf = NeutronConf(context_wrap(NEUTRON_CONF))
    assert nconf is not None
    assert list(nconf.sections()) == ['quotas', 'agent', 'keystone_authtoken', 'database', 'service_providers']
    assert nconf.defaults() == {'debug': 'False', 
       'verbose': 'False', 
       'core_plugin': 'neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2'}
    assert nconf.get('quotas', 'quota_network') == '10'
    assert nconf.has_option('database', 'connection')
    assert not nconf.has_option('yabba', 'dabba_do')
    assert nconf.get('DEFAULT', 'debug') == 'False'
    return
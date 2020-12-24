# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_heat_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.heat_conf import HeatConf
from insights.tests import context_wrap
HEAT_CONFIG = ('\n[DEFAULT]\nheat_metadata_server_url = http://172.16.0.11:8000\nheat_waitcondition_server_url = http://172.16.0.11:8000/v1/waitcondition\nheat_watch_server_url =http://172.16.0.11:8003\nstack_user_domain_name = heat_stack\nstack_domain_admin = heat_stack_domain_admin\nstack_domain_admin_password = *********\nauth_encryption_key = mysupersecretkey\nlog_dir = /var/log/heat\ninstance_user=\nnotification_driver=messaging\n[auth_password]\n[clients]\n[clients_ceilometer]\n[clients_cinder]\n[clients_glance]\n[clients_heat]\n[clients_keystone]\nauth_uri =http://192.0.2.18:35357\n[clients_neutron]\n[clients_nova]\n[clients_sahara]\n[clients_swift]\n[clients_trove]\n[cors]\n[cors.subdomain]\n[database]\nconnection = *********\n[ec2authtoken]\nauth_uri = http://172.16.0.11:5000/v2.0/ec2tokens\n[eventlet_opts]\n[heat_api]\nbind_host = 172.16.0.15\nworkers = 0\n[heat_api_cfn]\nbind_host = 172.16.0.15\nworkers = 0\n[heat_api_cloudwatch]\nbind_host = 172.16.0.15\nworkers = 0\n').strip()

def test_heat_conf():
    h_conf = HeatConf(context_wrap(HEAT_CONFIG))
    assert h_conf.get('DEFAULT', 'heat_metadata_server_url') == 'http://172.16.0.11:8000'
    assert h_conf.get('DEFAULT', 'stack_user_domain_name') == 'heat_stack'
    assert h_conf.get('clients_keystone', 'auth_uri') == 'http://192.0.2.18:35357'
    assert h_conf.get('heat_api_cloudwatch', 'bind_host') == '172.16.0.15'
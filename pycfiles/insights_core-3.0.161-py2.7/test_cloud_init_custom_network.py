# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cloud_init_custom_network.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import cloud_init_custom_network
from insights.parsers.cloud_init_custom_network import CloudInitCustomNetworking
from insights.tests import context_wrap
import doctest
CLOUD_INIT_CONFIG = '\nnetwork:\n    version: 1\n    config:\n    - type: physical\n      name: eth0\n      subnets:\n        - type: dhcp\n        - type: dhcp6\n'

def test_cloud_init_custom_network():
    result = cloud_init_custom_network.CloudInitCustomNetworking(context_wrap(CLOUD_INIT_CONFIG))
    assert result.data['network']['config'][0]['name'] == 'eth0'
    assert result.data['network']['config'][0]['subnets'][0]['type'] == 'dhcp'
    assert result.data['network']['config'][0]['subnets'][1]['type'] == 'dhcp6'


def test_cloud_init_custom_networks_doc_examples():
    env = {'cloud_init_custom_network_config': CloudInitCustomNetworking(context_wrap(CLOUD_INIT_CONFIG))}
    failed, total = doctest.testmod(cloud_init_custom_network, globs=env)
    assert failed == 0
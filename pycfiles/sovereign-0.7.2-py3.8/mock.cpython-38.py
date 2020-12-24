# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/utils/mock.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 803 bytes
from random import randint
from sovereign.schemas import DiscoveryRequest, Node, Locality

def mock_discovery_request(service_cluster=None, resource_names=None, region='none', version='1.11.1', metadata=None) -> DiscoveryRequest:
    if not isinstance(metadata, dict):
        metadata = dict()
    return DiscoveryRequest(node=Node(id='mock',
      cluster=(service_cluster or ''),
      build_version=f"e5f864a82d4f27110359daa2fbdcb12d99e415b9/{version}/Clean/RELEASE",
      locality=Locality(zone=region),
      metadata={**{'hide_private_keys': True}, **metadata}),
      version_info=(str(randint(100000, 1000000000))),
      resource_names=(resource_names or []))
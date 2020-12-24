# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/samples/openstack.py
# Compiled at: 2014-05-30 05:53:08
simple_tenant_usage_data = [
 {'total_volume_gb_usage': 480.0, 
    'total_memory_mb_usage': 393216.0, 
    'total_vcpus_usage': 192.0, 
    'start': '2012-09-05 00:00:00', 
    'tenant_id': 'e638ade19b0de826ee1391ee8e84dd7e', 
    'stop': '2012-09-06 00:00:00', 
    'total_hours': 48.0, 
    'total_local_gb_usage': 768.0, 
    'total_images_gb_usage': 199.3},
 {'total_volume_gb_usage': 28800.0, 
    'total_memory_mb_usage': 786432.0, 
    'total_vcpus_usage': 384.0, 
    'start': '2012-09-05 00:00:00', 
    'tenant_id': 'c6b791dae6baa644a71bed1a71615f2d', 
    'stop': '2012-09-06 00:00:00', 
    'total_hours': 96.0, 
    'total_local_gb_usage': 1536.0, 
    'total_images_gb_usage': 315.0},
 {'total_volume_gb_usage': 0, 
    'total_memory_mb_usage': 98304.0, 
    'total_vcpus_usage': 48.0, 
    'start': '2012-09-05 00:00:00', 
    'tenant_id': '8c9b6d8553c91ae6ad5023cfc1febb1c', 
    'stop': '2012-09-06 00:00:00', 
    'total_hours': 48.0, 
    'total_images_gb_usage': 45.0, 
    'total_local_gb_usage': 216.0}]
tenants_usages_data = {'tenant_usages': simple_tenant_usage_data}
tenants_data = {'tenants': [
             {'enabled': True, 
                'name': 'test_venture1', 
                'id': 'e638ade19b0de826ee1391ee8e84dd7e', 
                'description': 'venture:test_venture1;'},
             {'enabled': True, 
                'name': 'test_venture2', 
                'id': 'c6b791dae6baa644a71bed1a71615f2d', 
                'description': 'venture:test_venture2;'},
             {'enabled': False, 
                'name': 'test_venture3', 
                'id': '8c9b6d8553c91ae6ad5023cfc1febb1c', 
                'description': 'fake description;'}]}
tenants = {'e638ade19b0de826ee1391ee8e84dd7e': 'test_venture1', 
   'c6b791dae6baa644a71bed1a71615f2d': 'test_venture2'}
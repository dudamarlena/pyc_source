# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nova_conf.py
# Compiled at: 2019-05-16 13:41:33
from __future__ import print_function
from insights.core.context import OSP
from insights.parsers import nova_conf
from insights.tests import context_wrap
nova_content = '\n\n[DEFAULT]\nnotification_driver =\n#this is comment\n\nnotification_topics=notifications\n\nrpc_backend=rabbit\nuse_ipv6=True\nnotify_on_state_change=vm_and_task_state\nnotify_api_faults=False\nstate_path=/var/lib/nova\nreport_interval = 10\nosapi_compute_listen=fd00:4888:1000:f901::c1\nosapi_compute_workers=32\nmetadata_listen=fd00:4888:1000:f901::c1\nmetadata_workers=32\nservice_down_time=60\nrootwrap_config=/etc/nova/rootwrap.conf\nauth_strategy=keystone\nuse_forwarded_for=False\nnovncproxy_host=fd00:4888:1000:f901::c1\nnovncproxy_port=6080\nnetwork_api_class=nova.network.neutronv2.api.API\ndhcp_domain=\nsecurity_group_api=neutron\ndebug=False\nverbose=False\nlog_dir=/var/log/nova\nuse_syslog=False\nscheduler_host_manager=nova.scheduler.host_manager.HostManager\nscheduler_host_subset_size=1\ncpu_allocation_ratio=16.0\ndisk_allocation_ratio=1.0\nmax_io_ops_per_host=8\nmax_instances_per_host=50\nram_allocation_ratio=1.0\nscheduler_available_filters=nova.scheduler.filters.all_filters\nscheduler_default_filters=RetryFilter,AvailabilityZoneFilter,RamFilter,ComputeFilter,ComputeCapabilitiesFilter,ImagePropertiesFilter,ServerGroupAntiAffinityFilter,ServerGroupAffinityFilter,NUMATopologyFilter,PciPassthroughFilter\nscheduler_weight_classes=nova.scheduler.weights.all_weighers\nscheduler_max_attempts=3\nvif_plugging_is_fatal=True\nvif_plugging_timeout=300\nfirewall_driver=nova.virt.firewall.NoopFirewallDriver\nnovncproxy_base_url=http://[fd00:4888:1000:f901::c1]:6080/vnc_auto.html\nvolume_api_class=nova.volume.cinder.API\nmemcached_servers=inet6:[fd00:4888:1000:f901::c0]:11211,inet6:[fd00:4888:1000:f901::c1]:11211,inet6:[fd00:4888:1000:f901::c2]:11211\n[ephemeral_storage_encryption]\n[glance]\napi_servers=http://[fd00:4888:1000:f901::a000]:9292\n[keystone_authtoken]\nauth_uri=http://[fd00:4888:1000:f901::a000]:5000/v2.0\nidentity_uri=http://192.168.1.107:35357\nadmin_user=nova\nadmin_password=*********\nadmin_tenant_name=service\nservice_metadata_proxy=True\novs_bridge=br-int\nextension_sync_interval=600\nrabbit_hosts=fd00:4888:1000:f901::c0,fd00:4888:1000:f901::c1,fd00:4888:1000:f901::c2\nrabbit_use_ssl=False\nrabbit_userid=guest\nrabbit_password=*********\nrabbit_virtual_host  =  /\nrabbit_ha_queues=True\nheartbeat_timeout_threshold=60\nheartbeat_rate=2\n'
osp = OSP()
osp.role = 'Compute'

def test_nova_conf():
    result = nova_conf.NovaConf(context_wrap(nova_content, osp=osp))
    print(result)
    assert result.get('DEFAULT', 'notification_driver') == ''
    assert result.get('DEFAULT', 'report_interval') == '10'
    assert result.get('DEFAULT', 'novncproxy_host') == 'fd00:4888:1000:f901::c1'
    assert result.get('keystone_authtoken', 'auth_uri') == 'http://[fd00:4888:1000:f901::a000]:5000/v2.0'
    assert result.get('keystone_authtoken', 'service_metadata_proxy') == 'True'
    assert result.get('keystone_authtoken', 'rabbit_hosts') == 'fd00:4888:1000:f901::c0,fd00:4888:1000:f901::c1,fd00:4888:1000:f901::c2'
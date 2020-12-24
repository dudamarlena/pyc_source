# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ironic_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ironic_conf
from insights.parsers.ironic_conf import IronicConf
from insights.tests import context_wrap
ironic_content = '\n[DEFAULT]\nauth_strategy=keystone\ndefault_resource_class=baremetal\nenabled_hardware_types=idrac,ilo,ipmi,redfish\nenabled_bios_interfaces=no-bios\nenabled_boot_interfaces=ilo-pxe,pxe\nenabled_console_interfaces=ipmitool-socat,ilo,no-console\nenabled_deploy_interfaces=iscsi,direct,ansible\nenabled_inspect_interfaces=inspector,no-inspect\ndefault_inspect_interface=inspector\nenabled_management_interfaces=fake,idrac,ilo,ipmitool,noop,redfish\nenabled_network_interfaces=flat\ndefault_network_interface=flat\nenabled_power_interfaces=fake,idrac,ilo,ipmitool,redfish\nenabled_raid_interfaces=idrac,no-raid\nenabled_rescue_interfaces=no-rescue,agent\ndefault_rescue_interface=agent\nenabled_storage_interfaces=noop\nenabled_vendor_interfaces=idrac,ipmitool,no-vendor\nmy_ip=192.168.24.1\ndebug=True\nlog_dir=/var/log/ironic\n[agent]\ndeploy_logs_collect=always\ndeploy_logs_storage_backend=local\ndeploy_logs_local_path=/var/log/ironic/deploy/\n[ansible]\n[api]\n[audit]\n[cimc]\n[cinder]\nauth_type=password\npassword=Nzmsp57Yg94HXsv9x8Znc7tEI\nproject_domain_name=Default\nproject_name=service\nuser_domain_name=Default\nusername=ironic\n[cisco_ucs]\n[conductor]\nforce_power_state_during_sync=False\nautomated_clean=False\nmax_time_interval=120\n[console]\n[cors]\nallowed_origin=*\nexpose_headers=Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma\nmax_age=3600\nallow_methods=GET,POST,PUT,DELETE,OPTIONS,PATCH\nallow_headers=Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma,X-Auth-Token\n[database]\n[deploy]\nhttp_root=/var/lib/ironic/httpboot\nerase_devices_priority=0\nerase_devices_metadata_priority=10\n'

def test_ironic_conf():
    result = IronicConf(context_wrap(ironic_content))
    assert result.get('DEFAULT', 'auth_strategy') == 'keystone'
    assert result.get('DEFAULT', 'default_resource_class') == 'baremetal'
    assert result.get('DEFAULT', 'default_rescue_interface') == 'agent'
    assert result.get('agent', 'deploy_logs_collect') == 'always'
    assert result.get('conductor', 'force_power_state_during_sync') == 'False'


def test_ironic_conf_docs():
    failed, total = doctest.testmod(ironic_conf, globs={'ironic_conf': IronicConf(context_wrap(ironic_content))})
    assert failed == 0
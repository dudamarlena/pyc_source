# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_openshift_hosts.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import openshift_hosts
from insights.tests import context_wrap
OPENSHIFTHOSTS = ('\n[OSEv3:children]\nnodes\nnfs\nmasters\netcd\n\n[BlankTest]\n\n[OSEv3:vars]\nopenshift_master_cluster_public_hostname=None\nansible_ssh_user=root\nopenshift_master_cluster_hostname=None\nopenshift_hostname_check=false\ndeployment_type=openshift-enterprise\n\n[nodes]\nmaster.ose35.com  openshift_public_ip=192.66.208.202 openshift_ip=192.66.208.202 openshift_public_hostname=master.ose35.com openshift_hostname=master.ose35.com connect_to=master.ose35.com openshift_schedulable=False ansible_connection=local\nnode1.ose35.com  openshift_public_ip=192.66.208.169 openshift_ip=192.66.208.169 openshift_public_hostname=node1.ose35.com openshift_hostname=node1.ose35.com connect_to=node1.ose35.com openshift_node_labels="{\'region\': \'infra\',\'zone\': \'default\'}" openshift_schedulable=True\nnode2.ose35.com  openshift_public_ip=192.66.208.170 openshift_ip=192.66.208.170 openshift_public_hostname=node2.ose35.com openshift_hostname=node2.ose35.com connect_to=node2.ose35.com openshift_node_labels="{\'region\': \'infra\',\'zone\': \'default\'}" openshift_schedulable=True\n\n[nfs]\nmaster.ose35.com  openshift_public_ip=192.66.208.202 openshift_ip=192.66.208.202 openshift_public_hostname=master.ose35.com openshift_hostname=master.ose35.com connect_to=master.ose35.com ansible_connection=local\n\n[masters]\nmaster.ose35.com  openshift_public_ip=192.66.208.202 openshift_ip=192.66.208.202 openshift_public_hostname=master.ose35.com openshift_hostname=master.ose35.com connect_to=master.ose35.com ansible_connection=local\n\n[etcd]\nmaster.ose35.com  openshift_public_ip=192.66.208.202 openshift_ip=192.66.208.202 openshift_public_hostname=master.ose35.com openshift_hostname=master.ose35.com connect_to=master.ose35.com ansible_connection=local\n').strip()

def test_openshifthosts():
    host_info = openshift_hosts.OpenShiftHosts(context_wrap(OPENSHIFTHOSTS))
    assert host_info['OSEv3:children'] == ['nodes', 'nfs', 'masters', 'etcd']
    assert host_info['OSEv3:vars']['ansible_ssh_user'] == 'root'
    assert host_info['nodes']['master.ose35.com']['openshift_public_ip'] == '192.66.208.202'
    assert host_info['nodes']['node1.ose35.com']['openshift_node_labels'] == {'region': 'infra', 'zone': 'default'}
    assert host_info.has_node('node1.ose35.com')
    assert not host_info.has_var('openshift_use_crio')
    assert host_info.has_node_type('etcd')
    assert host_info['BlankTest'] == {}
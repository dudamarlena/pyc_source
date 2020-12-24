# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rabbitmq_report.py
# Compiled at: 2019-11-14 13:57:46
from insights.core.context import OSP
from insights.contrib.pyparsing import ParseException as PyparsingParseException
from insights.parsers.rabbitmq import RabbitMQReport, RabbitMQReportOfContainers
from insights.tests import context_wrap
osp_controller = OSP()
osp_controller.role = 'Controller'
RABBITMQCTL_REPORT_0 = "\nError: unable to connect to node rabbit@dprcclab002: nodedown\n\nDIAGNOSTICS\n===========\n\nattempted to contact: [rabbit@dprcclab002]\n\nrabbit@dprcclab002:\n  * connected to epmd (port 4369) on dprcclab002\n  * epmd reports: node 'rabbit' not running at all\n                  no other nodes on dprcclab002\n  * suggestion: start the node\n\ncurrent node details:\n- node name: 'rabbitmq-cli-08@dprcclab002'\n- home dir: /var/lib/rabbitmq\n- cookie hash: k0XaAkNZ29GQG22RA/Uyxw==\n"
RABBITMQCTL_REPORT_1 = '\nReporting server status on {{2016,10,17},{3,42,41}}\n\n ...\nStatus of node rabbit@rabbitmq0 ...\n[{pid,5085},\n {os,{unix,linux}},\n {erlang_version,\n     "Erlang R16B03-1 (erts-5.10.4) [source] [64-bit] [smp:4:4] [async-threads:30] [hipe] [kernel-poll:true]\n"},\n {listeners,[{clustering,25672,"::"},{amqp,5672,"::"}]},\n {vm_memory_high_watermark,0.4},\n {vm_memory_limit,1590132736},\n {disk_free_limit,50000000},\n {disk_free,40712921088},\n {file_descriptors,\n     [{total_limit,924},{total_used,3},{sockets_limit,829},{sockets_used,1}]},\n {processes,[{limit,1048576},{used,180}]},\n {run_queue,0},\n {uptime,5590}]\n\nCluster status of node rabbit@rabbitmq0 ...\n[{nodes,[{disc,[rabbit@rabbitmq0]}]},\n\nApplication environment of node rabbit@rabbitmq0 ...\n[{auth_backends,[rabbit_auth_backend_internal]},\n\nPermissions on /:\nuser    configure       write   read\nguest   .*      .*      .*\nredhat  redhat.*        .*      .*\nredhat1 redhat.*        .*      .*\n\nPermissions on test_vhost:\n\nPolicies on /:\n\nPolicies on test_vhost:\n\n...done.\n'
RABBITMQCTL_REPORT_2 = '\nReporting server status on {{2016,4,26},{6,51,27}}\n\n ...\nStatus of node \'rabbit@overcloud-controller-2\' ...\n[{pid,4087},\n {vm_memory_limit,26943271731},\n {disk_free_limit,50000000},\n {disk_free,257304219648},\n {file_descriptors,[{total_limit,3996},\n                    {total_used,835},\n                    {sockets_limit,3594},\n                    {sockets_used,833}]},\n {uptime,3075474}]\n\nCluster status of node \'rabbit@overcloud-controller-2\' ...\n[{nodes,[{disc,[\'rabbit@overcloud-controller-0\',\n                \'rabbit@overcloud-controller-1\',\n                \'rabbit@overcloud-controller-2\']}]},\n {partitions,[]}]\n\nApplication environment of node \'rabbit@overcloud-controller-2\' ...\n[{auth_backends,[rabbit_auth_backend_internal]}]\n\nStatus of node \'rabbit@overcloud-controller-1\' ...\n[{pid,9304},\n {disk_free_limit,50000000},\n {disk_free,260561866752},\n {file_descriptors,[{total_limit,3996},\n                    {total_used,853},\n                    {sockets_limit,3594},\n                    {sockets_used,851}]},\n {uptime,3075482}]\n\nCluster status of node \'rabbit@overcloud-controller-2\' ...\n[{nodes,[{disc,[\'rabbit@overcloud-controller-0\',\n                \'rabbit@overcloud-controller-1\',\n                \'rabbit@overcloud-controller-2\']}]},\n {partitions,[]}]\n\nApplication environment of node \'rabbit@overcloud-controller-2\' ...\n[{auth_backends,[rabbit_auth_backend_internal]}]\n\nStatus of node \'rabbit@overcloud-controller-0\' ...\n[{pid,6005},\n {disk_free_limit,50000000},\n {disk_free,259739344896},\n {file_descriptors,[{total_limit,3996},\n                    {total_used,967},\n                    {sockets_limit,3594},\n                    {sockets_used,965}]},\n {uptime,3075485}]\n\nCluster status of node \'rabbit@overcloud-controller-2\' ...\n[{nodes,[{disc,[\'rabbit@overcloud-controller-0\',\n                \'rabbit@overcloud-controller-1\',\n                \'rabbit@overcloud-controller-2\']}]},\n {partitions,[]}]\n\nApplication environment of node \'rabbit@overcloud-controller-2\' ...\n[{auth_backends,[rabbit_auth_backend_internal]}]\n\nPermissions on /:\nuser\tconfigure\twrite\tread\nguest\t.*\t.*\t.*\n\nPolicies on /:\nvhost\tname\tapply-to\tpattern\tdefinition\tpriority\n/\tha-all\tall\t^(?!amq\\.).*\t{"ha-mode":"all"}\t0\n\nParameters on /:\n\n...done.\n'
RABBITMQCTL_REPORT_3 = '\nReporting server status on {{2019,5,2},{18,57,48}}\n\n ...\nStatus of node rabbit@controller1 ...\n[{pid,76101},\n {running_applications,[{rabbit,"RabbitMQ","3.6.3"},\n                        {os_mon,"CPO  CXC 138 46","2.4"},\n                        {rabbit_common,[],"3.6.3"},\n                        {mnesia,"MNESIA  CXC 138 12","4.13.4"},\n                        {ranch,"Socket acceptor pool for TCP protocols.",\n                               "1.2.1"},\n                        {xmerl,"XML parser","1.3.10"},\n                        {sasl,"SASL  CXC 138 11","2.7"},\n                        {stdlib,"ERTS  CXC 138 10","2.8"},\n                        {kernel,"ERTS  CXC 138 10","4.2"}]},\n {os,{unix,linux}},\n {erlang_version,"Erlang/OTP 18 [erts-7.3.1.2] [source] [64-bit] [smp:56:56] [async-threads:896] [hipe] [kernel-poll:true]\\n"},\n {memory,[{total,7198193032},\n          {connection_readers,2582888},\n          {connection_writers,611032},\n          {connection_channels,3622776},\n          {connection_other,6805920},\n          {queue_procs,113304336},\n          {queue_slave_procs,2454511224},\n          {plugins,0},\n          {other_proc,59823544},\n          {mnesia,18861888},\n          {mgmt_db,0},\n          {msg_index,2912704},\n          {other_ets,3109632},\n          {binary,4460926336},\n          {code,19689791},\n          {atom,752537},\n          {other_system,50678424}]},\n {alarms,[]},\n {listeners,[{clustering,25672,"::"},{amqp,5672,"172.16.64.62"}]},\n {vm_memory_high_watermark,0.4},\n {vm_memory_limit,162189606912},\n {disk_free_limit,50000000},\n {disk_free,151495786496},\n {file_descriptors,[{total_limit,16284},\n                    {total_used,222},\n                    {sockets_limit,14653},\n                    {sockets_used,220}]},\n {processes,[{limit,1048576},{used,16029}]},\n {run_queue,0},\n {uptime,1986766},\n {kernel,{net_ticktime,60}}]\n\nCluster status of node rabbit@controller1 ...\n[{nodes,[{disc,[rabbit@controller0,rabbit@controller1,rabbit@controller2]}]},\n {running_nodes,[rabbit@controller0,rabbit@controller2,rabbit@controller1]},\n {cluster_name,<<"rabbit@controller0.external.s4-southlake.vcp.vzwops.com">>},\n {partitions,[]},\n {alarms,[{rabbit@controller0,[]},\n          {rabbit@controller2,[]},\n          {rabbit@controller1,[]}]}]\n\nPermissions on /:\nuser\tconfigure\twrite\tread\nguest\t.*\t.*\t.*\n\nPolicies on /:\nvhost\tname\tapply-to\tpattern\tdefinition\tpriority\n/\tha-all\tall\t^(?!amq\\.).*\t{"ha-mode":"all"}\t0\n\nParameters on /:\n\n...done.\n\n'

def test_rabbitmq_report():
    result = RabbitMQReport(context_wrap(RABBITMQCTL_REPORT_1, hostname='controller_1', osp=osp_controller)).result
    assert result.get('nstat').get('rabbit@rabbitmq0').get('file_descriptors').get('total_limit') == '924'
    permissions = {'/': {'redhat1': ['redhat.*', '.*', '.*'], 'guest': [
                     '.*', '.*', '.*'], 
             'redhat': [
                      'redhat.*', '.*', '.*']}, 
       'test_vhost': ''}
    assert result.get('perm') == permissions
    result = RabbitMQReport(context_wrap(RABBITMQCTL_REPORT_2, hostname='controller_1', osp=osp_controller)).result
    assert result.get('nstat').get("'rabbit@overcloud-controller-2'").get('file_descriptors').get('total_limit') == '3996'
    assert len(result.get('nstat')) == 3
    permissions = {'/': {'guest': ['.*', '.*', '.*']}}
    assert result.get('perm') == permissions
    result = RabbitMQReport(context_wrap(RABBITMQCTL_REPORT_3, hostname='controller_1', osp=osp_controller)).result
    assert result.get('nstat').get('rabbit@controller1').get('file_descriptors').get('total_limit') == '16284'
    assert len(result.get('nstat')) == 1
    assert result.get('nstat').get('rabbit@controller1').get('erlang_version')[(-1)] == '[kernel-poll:true]\\n"'


def test_rabbitmq_report_with_parse_exception():
    try:
        RabbitMQReport(context_wrap(RABBITMQCTL_REPORT_0, hostname='controller_1', osp=osp_controller))
        assert False
    except PyparsingParseException:
        assert True


def test_rabbitmq_report_of_containers():
    result = RabbitMQReportOfContainers(context_wrap(RABBITMQCTL_REPORT_1, hostname='controller_1', osp=osp_controller)).result
    assert result.get('nstat').get('rabbit@rabbitmq0').get('file_descriptors').get('total_limit') == '924'
    permissions = {'/': {'redhat1': ['redhat.*', '.*', '.*'], 'guest': [
                     '.*', '.*', '.*'], 
             'redhat': [
                      'redhat.*', '.*', '.*']}, 
       'test_vhost': ''}
    assert result.get('perm') == permissions
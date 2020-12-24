# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/describe_alarm_policies.py
# Compiled at: 2017-11-28 05:16:19
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeAlarmPoliciesAction(BaseAction):
    action = 'DescribeAlarmPolicies'
    command = 'describe-alarm-policies'
    usage = '%(prog)s [-a <alarm_policies> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policies', dest='alarm_policies', action='store', type=str, default=None, help='id IDs of alarm policies you want to describe.')
        parser.add_argument('-n', '--alarm-policy-name', dest='alarm_policy_name', action='store', type=str, default=None, help='the name of alarm policy.')
        parser.add_argument('-t', '--alarm-policy-type', dest='alarm_policy_type', action='store', type=str, default=None, help='valid values includes instance, eip, router, loadbalancer_listener_http, loadbalancer_listener_tcp, loadbalancer_backend_http, loadbalancer_backend_tcp.')
        parser.add_argument('-s', '--search-word', dest='search_word', action='store', type=str, default=None, help='you can use this field to search from id or name.')
        parser.add_argument('-r', '--resource', dest='resource', action='store', type=str, default=None, help='the ID of resource associated to this policy.')
        parser.add_argument('-S', '--status', dest='status', action='store', type=str, default=None, help='valid values includes active, suspended.')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store', type=int, default=None, help='the number to specify the verbose level,')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'alarm_policies': explode_array(options.alarm_policies), 
           'alarm_policy_name': options.alarm_policy_name, 
           'alarm_policy_type': options.alarm_policy_type, 
           'search_word': options.search_word, 
           'resource': options.resource, 
           'status': explode_array(options.status), 
           'verbose': options.verbose}
        return directive
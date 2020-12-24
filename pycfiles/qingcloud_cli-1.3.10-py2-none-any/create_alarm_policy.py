# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/create_alarm_policy.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateAlarmPolicyAction(BaseAction):
    action = 'CreateAlarmPolicy'
    command = 'create-alarm-policy'
    usage = '%(prog)s [-t <alarm_policy_type> ...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--alarm-policy-type', dest='alarm_policy_type', action='store', type=str, default='', help='valid values includes instance,eip,router,loadbalancer_listener_http,loadbalancer_listener_tcp,loadbalancer_backend_http,loadbalancer_backend_tcp.')
        parser.add_argument('-p', '--period', dest='period', action='store', type=str, default='', help='the period of alarm_policy. For example: One minute : 1m.')
        parser.add_argument('-n', '--alarm-policy-name', dest='alarm_policy_name', action='store', type=str, default=None, help='the name of alarm policy.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.alarm_policy_type == '':
            print 'error: alarm_policy_type should be specified.'
            return None
        else:
            if options.period == '':
                print 'error: period should be specified.'
                return None
            directive = {'alarm_policy_type': options.alarm_policy_type, 
               'period': options.period, 
               'alarm_policy_name': options.alarm_policy_name}
            return directive
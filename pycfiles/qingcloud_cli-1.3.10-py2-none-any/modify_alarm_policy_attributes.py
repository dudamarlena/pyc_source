# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/modify_alarm_policy_attributes.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyAlarmPolicyAttributesAction(BaseAction):
    action = 'ModifyAlarmPolicyAttributes'
    command = 'modify-alarm-policy-attributes'
    usage = '%(prog)s [-a <alarm_policy> ] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policy', dest='alarm_policy', action='store', type=str, default='', help='the ID of alarm policy.')
        parser.add_argument('-p', '--period', dest='period', action='store', type=str, default=None, help='the period of alarm policy. For example: One minute : 1m.')
        parser.add_argument('-n', '--alarm-policy-name', dest='alarm_policy_name', action='store', type=str, default=None, help='the name of alarm policy.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the description of alarm policy.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.alarm_policy == '':
            print 'error: alarm_policy should be specified.'
            return None
        else:
            directive = {'alarm_policy': options.alarm_policy, 
               'period': options.period, 
               'alarm_policy_name': options.alarm_policy_name, 
               'description': options.description}
            return directive
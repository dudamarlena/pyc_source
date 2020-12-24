# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/describe_alarm_policy_rules.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeAlarmPolicyRulesAction(BaseAction):
    action = 'DescribeAlarmPolicyRules'
    command = 'describe-alarm-policy-rules'
    usage = '%(prog)s [-a <alarm_policy> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policy', dest='alarm_policy', action='store', type=str, default=None, help='the ID of alarm_policy.')
        parser.add_argument('-r', '--alarm-policy-rules', dest='alarm_policy_rules', action='store', type=str, default=None, help='an array including IDs of alarm policy rules.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'alarm_policy_rules': explode_array(options.alarm_policy_rules), 
           'alarm_policy': options.alarm_policy, 
           'offset': options.offset, 
           'limit': options.limit}
        return directive
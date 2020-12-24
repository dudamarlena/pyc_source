# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/modify_alarm_policy_rule_attributes.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyAlarmPolicyRuleAttributesAction(BaseAction):
    action = 'ModifyAlarmPolicyRuleAttributes'
    command = 'modify-alarm-policy-rule-attributes'
    usage = '%(prog)s [-r <alarm_policy_rule>...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--alarm-policy-rule', dest='alarm_policy_rule', action='store', type=str, default='', help='the ID of the alarm policy rule whose content you want to update.')
        parser.add_argument('-c', '--condition-type', dest='condition_type', action='store', type=str, default='', help="'gt' for greater than, 'lt' for less than.")
        parser.add_argument('-n', '--alarm-policy-rule-name', dest='alarm_policy_rule_name', action='store', type=str, default=None, help='the name of alarm policy rule.')
        parser.add_argument('-t', '--thresholds', dest='thresholds', action='store', type=str, default=None, help='the thresholds of alarm.')
        parser.add_argument('-d', '--data-processor', dest='data_processor', action='store', type=str, default=None, help='raw for use the monitoring data raw value, percent only for IP bandwidth monitoring.')
        parser.add_argument('-p', '--consecutive_periods', dest='consecutive_periods', action='store', type=str, default=None, help='uring several consecutive inspection periods, the monitoring data reaches the alarm threshold,then will trigger the alarm behavior.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.alarm_policy_rule == '':
            print 'error: alarm_policy_rule should be specified.'
            return None
        else:
            if options.condition_type == '':
                print 'error: condition_type should be specified.'
                return None
            directive = {'alarm_policy_rule': options.alarm_policy_rule, 
               'condition_type': options.condition_type, 
               'alarm_policy_rule_name': options.alarm_policy_rule_name, 
               'thresholds': options.thresholds, 
               'data_processor': options.data_processor, 
               'consecutive_periods': options.consecutive_periods}
            return directive
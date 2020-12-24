# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/modify_alarm_policy_action_attributes.py
# Compiled at: 2017-11-28 04:33:31
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyAlarmPolicyActionAttributesAction(BaseAction):
    action = 'ModifyAlarmPolicyActionAttributes'
    command = 'modify-alarm-policy-action-attributes'
    usage = '%(prog)s [-a <alarm_policy_action>...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policy-action', dest='alarm_policy_action', action='store', type=str, default='', help='the ID of the alarm policy action whose content you want to update.')
        parser.add_argument('-A', '--trigger-action', dest='trigger_action', action='store', type=str, default=None, help='the ID of the trigger action.')
        parser.add_argument('-s', '--trigger-status', dest='trigger_status', action='store', type=str, default=None, help="when the monitor alarm state becomes 'ok' or 'alarm', the message will be sent to this trigger list.")
        return

    @classmethod
    def build_directive(cls, options):
        if options.alarm_policy_action == '':
            print 'error: alarm_policy_action should be specified.'
            return None
        else:
            directive = {'alarm_policy_action': options.alarm_policy_action, 
               'trigger_action': options.trigger_action, 
               'trigger_status': options.trigger_status}
            return directive
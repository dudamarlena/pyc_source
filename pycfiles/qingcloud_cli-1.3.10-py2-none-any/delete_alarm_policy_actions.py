# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/delete_alarm_policy_actions.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.iaas_client.actions.base import BaseAction
from qingcloud.cli.misc.utils import explode_array

class DeleteAlarmPolicyActionsAction(BaseAction):
    action = 'DeleteAlarmPolicyActions'
    command = 'delete-alarm-policy-actions'
    usage = '%(prog)s [-a <alarm_policy_actions> ] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policy-actions', dest='alarm_policy_actions', action='store', type=str, default='', help='an array including IDs of alarm policy actions.')

    @classmethod
    def build_directive(cls, options):
        alarm_policy_actions = explode_array(options.alarm_policy_actions)
        if not alarm_policy_actions:
            print 'error: alarm_policy_actions should be specified.'
            return None
        else:
            directive = {'alarm_policy_actions': alarm_policy_actions}
            return directive
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/add_alarm_policy_actions.py
# Compiled at: 2017-11-28 04:06:50
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AddAlarmPolicyActionsAction(BaseAction):
    action = 'AddAlarmPolicyActions'
    command = 'add-alarm-policy-actions'
    usage = '%(prog)s [-a <alarm_policy>...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policy', dest='alarm_policy', action='store', type=str, default='', help='the ID of the alarm policy whose rules you want to add.')
        parser.add_argument('-A', '--actions', dest='actions', action='store', type=str, default='', help="it's a JSON list of actions you want to add.")

    @classmethod
    def build_directive(cls, options):
        if options.alarm_policy == '':
            print 'error: alarm_policy should be specified.'
            return None
        else:
            if options.actions == '':
                print 'error: actions should be specified.'
                return None
            directive = {'alarm_policy': options.alarm_policy, 
               'actions': json.loads(options.actions)}
            return directive
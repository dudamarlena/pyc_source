# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/describe_alarm_history.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeAlarmHistoryAction(BaseAction):
    action = 'DescribeAlarmHistory'
    command = 'describe-alarm-history'
    usage = '%(prog)s [-a <alarm> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm', dest='alarm', action='store', type=str, default='', help=' the ID of the resource alarm entity.')
        parser.add_argument('-t', '--history-type', dest='history_type', action='store', type=str, default=None, help='the types including trigger_action, status_change and config_update.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'alarm': options.alarm, 
           'history_type': options.history_type}
        return directive
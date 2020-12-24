# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/describe_alarms.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeAlarmsAction(BaseAction):
    action = 'DescribeAlarms'
    command = 'describe-alarms'
    usage = '%(prog)s [-a <alarms> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarms', dest='alarms', action='store', type=str, default=None, help='an array including IDs of the alarms you want to list.')
        parser.add_argument('-p', '--policy', dest='policy', action='store', type=str, default=None, help=' the ID of alarm policy.')
        parser.add_argument('-r', '--resource', dest='resource', action='store', type=str, default=None, help='the ID of resource associated to this policy.')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default=None, help='ok stand for normal,alarm stand for alarming,insufficient stand for monitoring data cannot be collected.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'alarms': explode_array(options.alarms), 
           'policy': options.policy, 
           'resource': options.resource, 
           'status': options.status}
        return directive
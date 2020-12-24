# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/delete_alarm_policies.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteAlarmPoliciesAction(BaseAction):
    action = 'DeleteAlarmPolicies'
    command = 'delete-alarm-policies'
    usage = '%(prog)s [-a alarm-policies] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policies', dest='alarm_policies', action='store', type=str, default='', help='an array including IDs of alarm policies.')

    @classmethod
    def build_directive(cls, options):
        alarm_policies = explode_array(options.alarm_policies)
        if not alarm_policies:
            print 'error: [alarm_policies] should be specified'
            return None
        else:
            directive = {'alarm_policies': alarm_policies}
            return directive
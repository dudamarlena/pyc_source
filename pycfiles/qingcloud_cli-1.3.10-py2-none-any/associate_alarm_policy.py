# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/alarm_policy/associate_alarm_policy.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AssociateAlarmPolicyAction(BaseAction):
    action = 'AssociateAlarmPolicy'
    command = 'associate-alarm-policy'
    usage = '%(prog)s [-a <alarm_policy>...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-a', '--alarm-policy', dest='alarm_policy', action='store', type=str, default='', help='the ID of alarm policy.')
        parser.add_argument('-r', '--resources', dest='resources', action='store', type=str, default='', help='the ID of resources you want to associate with alarm policy.')
        parser.add_argument('-R', '--related-resource', dest='related_resource', action='store', type=str, default=None, help='when the network load balancer is bound,related_resource needs to specify a public network IP ID associated with this load balancer.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.alarm_policy == '':
            print 'error: alarm_policy should be specified.'
            return None
        else:
            resources = explode_array(options.resources)
            if not resources:
                print 'error: resources should be specified'
                return None
            directive = {'alarm_policy': options.alarm_policy, 
               'resources': resources, 
               'related_resource': options.related_resource}
            return directive
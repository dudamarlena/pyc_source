# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/describe_s2_default_parameters.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeS2DefaultParametersAction(BaseAction):
    action = 'DescribeS2DefaultParameters'
    command = 'describe-s2-default-parameters'
    usage = '%(prog)s [-T <service_type> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-T', '--service-type', dest='service_type', action='store', type=str, default=None, help='valid values is vsan or vnas.')
        parser.add_argument('-t', '--target-type', dest='target_type', action='store', type=str, default=None, help='valid values is ISCSI, FCoE, NFS or SMB.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'service_type': options.service_type, 
           'target_type': options.target_type}
        return directive
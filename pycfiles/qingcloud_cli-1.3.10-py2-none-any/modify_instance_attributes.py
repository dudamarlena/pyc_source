# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/instance/modify_instance_attributes.py
# Compiled at: 2015-05-26 14:05:30
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyInstanceAttributesAction(BaseAction):
    action = 'ModifyInstanceAttributes'
    command = 'modify-instance-attributes'
    usage = '%(prog)s -i <instance_id> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instance_id', dest='instance_id', action='store', type=str, default='', help='the id of the instance whose attributes you want to modify.')
        parser.add_argument('-N', '--instance_name', dest='instance_name', action='store', type=str, default=None, help='instance name')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='instance description')
        return parser

    @classmethod
    def build_directive(cls, options):
        if options.instance_id == '':
            print 'error:instance_id should be specified'
            return None
        else:
            return {'instance': options.instance_id, 
               'instance_name': options.instance_name, 
               'description': options.description}
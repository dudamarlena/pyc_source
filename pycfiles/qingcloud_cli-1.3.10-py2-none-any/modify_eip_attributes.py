# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/eip/modify_eip_attributes.py
# Compiled at: 2015-05-26 14:04:45
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyEipAttributesAction(BaseAction):
    action = 'ModifyEipAttributes'
    command = 'modify-eip-attributes'
    usage = '%(prog)s -e <eip_id> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--eip_id', dest='eip_id', action='store', type=str, default='', help='the id of the eip whose attributes you want to modify.')
        parser.add_argument('-n', '--eip_name', dest='eip_name', action='store', type=str, default=None, help='specify the new eip name.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.eip_id:
            return None
        else:
            return {'eip': options.eip_id, 
               'eip_name': options.eip_name, 
               'description': options.description}
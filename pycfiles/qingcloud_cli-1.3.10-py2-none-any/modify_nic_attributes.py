# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/nic/modify_nic_attributes.py
# Compiled at: 2017-05-07 03:27:36
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyNicAttributesAction(BaseAction):
    action = 'ModifyNicAttributes'
    command = 'modify-nic-attributes'
    usage = '%(prog)s -v nic_id [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-n', '--nic', dest='nic', action='store', type=str, default='', help='the id of the nic whose attributes you want to modify.')
        parser.add_argument('-N', '--nic-name', dest='nic_name', action='store', type=str, default=None, help='specify the new nic name.')
        parser.add_argument('-p', '--private-ip', dest='private_ip', action='store', type=str, default=None, help='the new private ip of nic.')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.nic:
            print 'error: [nic] should be specified'
            return None
        else:
            return {'nic': options.nic, 
               'nic_name': options.nic_name, 
               'private_ip': options.private_ip}
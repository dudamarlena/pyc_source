# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/keypair/modify_keypair_attributes.py
# Compiled at: 2015-05-26 14:06:22
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyKeyPairAttributesAction(BaseAction):
    action = 'ModifyKeyPairAttributes'
    command = 'modify-keypair-attributes'
    usage = '%(prog)s -k <keypair> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-k', '--keypair', dest='keypair', action='store', type=str, default='', help='the id of the keypair whose attributes you want to modify.')
        parser.add_argument('-N', '--keypair_name', dest='keypair_name', action='store', type=str, default=None, help='specify the new keypair name.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.keypair:
            return None
        else:
            return {'keypair': options.keypair, 
               'keypair_name': options.keypair_name, 
               'description': options.description}
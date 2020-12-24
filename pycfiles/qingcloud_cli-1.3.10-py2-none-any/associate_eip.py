# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/eip/associate_eip.py
# Compiled at: 2015-05-26 14:04:28
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AssociateEipAction(BaseAction):
    action = 'AssociateEip'
    command = 'associate-eip'
    usage = '%(prog)s -e <eip_id> -i <instance_id> [options] [-f <conf_file>]'
    description = 'Associate eip to instance'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--eip_id', dest='eip_id', action='store', type=str, default='', help='the id of the eip that you want to associate with instance.')
        parser.add_argument('-i', '--instance_id', dest='instance_id', action='store', type=str, default='', help='the instance you want to associate eip.')

    @classmethod
    def build_directive(cls, options):
        if not options.eip_id or not options.instance_id:
            print 'error: [eip] and [instance] should be specified'
            return None
        else:
            return {'eip': options.eip_id, 
               'instance': options.instance_id}
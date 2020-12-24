# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/keypair/detach_keypairs.py
# Compiled at: 2015-05-26 14:06:20
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DetachKeyPairsAction(BaseAction):
    action = 'DetachKeyPairs'
    command = 'detach-keypairs'
    usage = '%(prog)s --instances "instance_id, ..." --keypairs "kp_id, ..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-k', '--keypairs', dest='keypairs', action='store', type=str, default='', help='the comma separated IDs of keypairs you want to detach from instances. ')
        parser.add_argument('-i', '--instances', dest='instances', action='store', type=str, default='', help='the IDs of instances the keypairs will be detached from.')

    @classmethod
    def build_directive(cls, options):
        keypairs = explode_array(options.keypairs)
        instances = explode_array(options.instances)
        if not keypairs or not instances:
            return None
        return {'keypairs': keypairs, 
           'instances': instances}
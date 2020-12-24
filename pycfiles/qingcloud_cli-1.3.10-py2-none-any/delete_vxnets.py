# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/vxnet/delete_vxnets.py
# Compiled at: 2015-05-26 14:09:41
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteVxnetsAction(BaseAction):
    action = 'DeleteVxnets'
    command = 'delete-vxnet'
    usage = '%(prog)s --vxnets "vxnet_id, ..." [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--vxnets', dest='vxnets', action='store', type=str, default='', help='IDs of vxnets you want to delete.')

    @classmethod
    def build_directive(cls, options):
        vxnets = explode_array(options.vxnets)
        if not vxnets:
            print '[vxnets] should be specified.'
            return None
        else:
            return {'vxnets': vxnets}
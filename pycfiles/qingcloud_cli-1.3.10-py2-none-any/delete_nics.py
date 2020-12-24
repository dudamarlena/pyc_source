# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/nic/delete_nics.py
# Compiled at: 2017-05-07 03:28:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteNicsAction(BaseAction):
    action = 'DeleteNics'
    command = 'delete-nics'
    usage = '%(prog)s -v "nic_id,..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-n', '--nics', dest='nics', action='store', type=str, default='', help='the comma separated IDs of nics you want to delete.')

    @classmethod
    def build_directive(cls, options):
        if not options.nics:
            print 'error: [nics] should be specified'
            return None
        else:
            return {'nics': explode_array(options.nics)}
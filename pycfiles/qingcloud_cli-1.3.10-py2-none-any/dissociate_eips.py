# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/eip/dissociate_eips.py
# Compiled at: 2015-05-26 14:04:42
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DissociateEipsAction(BaseAction):
    action = 'DissociateEips'
    command = 'dissociate-eips'
    usage = '%(prog)s -e "eip_id, ..." [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--eips', dest='eips', action='store', type=str, default='', help='the comma separated IDs of eips you want to dissociate from instances.')

    @classmethod
    def build_directive(cls, options):
        eips = explode_array(options.eips)
        if not eips:
            return None
        else:
            return {'eips': eips}
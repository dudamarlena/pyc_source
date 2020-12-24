# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/nic/attach_nics.py
# Compiled at: 2017-05-07 03:28:22
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AttachNicsAction(BaseAction):
    action = 'AttachNics'
    command = 'attach-nics'
    usage = '%(prog)s -i <instance_id> -n "nic_id,..." [-f <conf_file>]'
    description = 'Attach one or more nics to instance'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instance', dest='instance', action='store', type=str, default=None, help='the ID of instance.')
        parser.add_argument('-n', '--nics', dest='nics', action='store', type=str, default='', help='the comma separated IDs of nics you want to attach.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'instance': options.instance, 
           'nics': options.nics}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'nics': explode_array(options.nics), 
           'instance': options.instance}
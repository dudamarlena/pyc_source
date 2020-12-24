# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/volume/modify_volume_attributes.py
# Compiled at: 2015-05-26 14:09:27
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyVolumeAttributesAction(BaseAction):
    action = 'ModifyVolumeAttributes'
    command = 'modify-volume-attributes'
    usage = '%(prog)s -v volume_id [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--volume_id', dest='volume_id', action='store', type=str, default='', help='the id of the volume whose attributes you want to modify.')
        parser.add_argument('-N', '--volume_name', dest='volume_name', action='store', type=str, default=None, help='specify the new volume name.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource.')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.volume_id:
            print 'error: [volumes_id] should be specified'
            return None
        else:
            return {'volume': options.volume_id, 
               'volume_name': options.volume_name, 
               'description': options.description}
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/image/capture_instance.py
# Compiled at: 2015-05-26 14:05:06
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CaptureInstanceAction(BaseAction):
    action = 'CaptureInstance'
    command = 'capture-instance'
    usage = '%(prog)s --instance <instance_id> --image_name <image_name> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instance', dest='instance', action='store', type=str, default=None, help='ID of the instance you want to capture.')
        parser.add_argument('-N', '--image_name', dest='image_name', action='store', type=str, default='', help='short name of the image.')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.instance:
            return None
        else:
            return {'instance': options.instance, 
               'image_name': options.image_name}
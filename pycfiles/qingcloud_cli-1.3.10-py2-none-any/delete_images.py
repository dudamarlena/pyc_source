# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/image/delete_images.py
# Compiled at: 2015-05-26 14:05:08
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteImagesAction(BaseAction):
    action = 'DeleteImages'
    command = 'delete-images'
    usage = '%(prog)s -i "image_id, ..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--images', dest='images', action='store', type=str, default='', help='the comma separated IDs of images you want to delete. ')

    @classmethod
    def build_directive(cls, options):
        images = explode_array(options.images)
        if not images:
            return None
        else:
            return {'images': images}
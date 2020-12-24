# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/tag/delete_tags.py
# Compiled at: 2015-10-28 03:08:01
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteTagsAction(BaseAction):
    action = 'DeleteTags'
    command = 'delete-tags'
    usage = '%(prog)s -k "tag_id, ..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--tags', dest='tags', action='store', type=str, default='', help='the comma separated IDs of tags you want to delete. ')

    @classmethod
    def build_directive(cls, options):
        tags = explode_array(options.tags)
        if not tags:
            return None
        else:
            return {'tags': tags}
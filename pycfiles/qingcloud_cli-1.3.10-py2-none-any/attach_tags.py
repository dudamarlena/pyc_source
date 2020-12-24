# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/tag/attach_tags.py
# Compiled at: 2015-10-28 03:08:01
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AttachTagsAction(BaseAction):
    action = 'AttachTags'
    command = 'attach-tags'
    usage = '%(prog)s --resource_tag_pairs "tag_id1:resource_type1:resource_id1;tag_id2:resource_type2:resource_id2..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-p', '--resource_tag_pairs', dest='resource_tag_pairs', action='store', type=str, default='', help='tag_id1:resource_type1:resource_id1;tag_id2:resource_type2:resource_id2...')

    @classmethod
    def build_directive(cls, options):
        resource_tag_pairs = explode_array(options.resource_tag_pairs, ';')
        for i, p in enumerate(resource_tag_pairs):
            tag_id, resource_type, resource_id = explode_array(p, ':')
            resource_tag_pairs[i] = {'tag_id': tag_id, 'resource_type': resource_type, 
               'resource_id': resource_id}

        directive = {'resource_tag_pairs': resource_tag_pairs}
        return directive
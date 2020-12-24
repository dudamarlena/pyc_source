# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/tag/modify_tag_attributes.py
# Compiled at: 2015-10-28 03:08:01
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyTagAttributesAction(BaseAction):
    action = 'ModifyTagAttributes'
    command = 'modify-tag-attributes'
    usage = '%(prog)s -t <tag> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--tag', dest='tag', action='store', type=str, default='', help='the id of the tag whose attributes you want to modify.')
        parser.add_argument('-N', '--tag_name', dest='tag_name', action='store', type=str, default=None, help='specify the new tag name.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.tag:
            return None
        else:
            return {'tag': options.tag, 'tag_name': options.tag_name, 
               'description': options.description}
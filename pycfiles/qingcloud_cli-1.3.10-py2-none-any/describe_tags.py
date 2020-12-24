# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/tag/describe_tags.py
# Compiled at: 2015-10-28 03:08:01
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeTagsAction(BaseAction):
    action = 'DescribeTags'
    command = 'describe-tags'
    usage = '%(prog)s [-t "tag_id, ..."] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--tags', dest='tags', action='store', type=str, default='', help='the ids of tags you want to list.')
        parser.add_argument('-W', '--search_word', dest='search_word', action='store', type=str, default='', help='the combined search column')
        parser.add_argument('-V', '--verbose', dest='verbose', action='store', type=int, default=0, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')

    @classmethod
    def build_directive(cls, options):
        return {'tags': explode_array(options.tags), 'search_word': options.search_word, 
           'verbose': options.verbose, 
           'offset': options.offset, 
           'limit': options.limit}
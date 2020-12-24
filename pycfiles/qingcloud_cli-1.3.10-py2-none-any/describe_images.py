# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/image/describe_images.py
# Compiled at: 2015-05-26 14:05:09
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeImagesAction(BaseAction):
    action = 'DescribeImages'
    command = 'describe-images'
    usage = '%(prog)s [-i "image_id, ..."] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--images', dest='images', action='store', type=str, default=None, help='the comma separated IDs of images you want to describe. ')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default=None, help='status: pending, available, deleted, ceased')
        parser.add_argument('-p', '--processor_type', dest='processor_type', action='store', type=str, default=None, help='filter by processor type, supported processor types are `64bit` and `32bit`')
        parser.add_argument('-F', '--os_family', dest='os_family', action='store', type=str, default=None, help='filter by OS family, supported values are windows/debian/centos/ubuntu.')
        parser.add_argument('-v', '--visibility', dest='visibility', action='store', type=str, default=None, help='filter by visibility, supported values are `public`, `private`')
        parser.add_argument('-W', '--search_word', dest='search_word', action='store', type=str, default=None, help='the combined search column')
        parser.add_argument('-P', '--provider', dest='provider', action='store', type=str, default=None, help='filter by the image provider, supported values are `self`, `system`')
        parser.add_argument('-V', '--verbose', dest='verbose', action='store', type=int, default=0, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')
        return

    @classmethod
    def build_directive(cls, options):
        return {'images': explode_array(options.images), 
           'processor_type': explode_array(options.processor_type), 
           'os_family': explode_array(options.os_family), 
           'visibility': explode_array(options.visibility), 
           'status': explode_array(options.status), 
           'provider': options.provider, 
           'verbose': options.verbose, 
           'search_word': options.search_word, 
           'offset': options.offset, 
           'limit': options.limit}
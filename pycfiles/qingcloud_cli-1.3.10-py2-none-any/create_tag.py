# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/tag/create_tag.py
# Compiled at: 2015-10-28 03:08:01
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateTagAction(BaseAction):
    action = 'CreateTag'
    command = 'create-tag'
    usage = '%(prog)s --tag_name <keypair_name> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-N', '--tag_name', dest='tag_name', action='store', type=str, default=None, help='name of the tag.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'tag_name': options.tag_name}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'param [%s] should be specified' % param
                return

        return {'tag_name': options.tag_name}
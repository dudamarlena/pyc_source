# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/modify_s2_server.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyS2ServerAttributesAction(BaseAction):
    action = 'ModifyS2ServerAttributes'
    command = 'modify-s2-server'
    usage = '%(prog)s -s <s2_server> [-n <s2_server_name> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-server', dest='s2_server', action='store', type=str, default=None, help='the ID of s2 server.')
        parser.add_argument('-n', '--s2-server-name', dest='s2_server_name', action='store', type=str, default=None, help='the new name you want to use.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the new value of description.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_server']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_server': options.s2_server, 's2_server_name': options.s2_server_name, 
           'description': options.description}
        return directive
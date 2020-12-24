# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/qs_client/actions/base.py
# Compiled at: 2017-02-22 02:44:19
import sys
from argparse import ArgumentParser
from qingcloud.qingstor.connection import QSConnection
from ...misc.utils import load_conf
from ..constants import DEFAULT_ENDPOINT

class BaseAction(object):
    command = ''
    usage = ''
    description = ''
    conn = None

    @classmethod
    def add_common_arguments(cls, parser):
        parser.add_argument('-f', '--config', dest='conf_file', action='store', type=str, default='~/.qingcloud/config.yaml', help='config file location')

    @classmethod
    def add_ext_arguments(cls, parser):
        pass

    @classmethod
    def get_argument_parser(cls):
        parser = ArgumentParser(prog='qingcloud qs %s' % cls.command, usage=cls.usage, description=cls.description)
        cls.add_common_arguments(parser)
        cls.add_ext_arguments(parser)
        return parser

    @classmethod
    def get_connection(cls, conf):
        endpoint = conf.get('endpoint', DEFAULT_ENDPOINT)
        if cls.command in ('create-bucket', 'list-buckets'):
            host = endpoint
        else:
            host = '%s.%s' % (conf['zone'], endpoint)
        return QSConnection(qy_access_key_id=conf['qy_access_key_id'], qy_secret_access_key=conf['qy_secret_access_key'], host=host)

    @classmethod
    def send_request(cls, options):
        return

    @classmethod
    def main(cls, args):
        parser = cls.get_argument_parser()
        options = parser.parse_args(args)
        conf = load_conf(options.conf_file)
        if conf is None:
            sys.exit(-1)
        cls.conn = cls.get_connection(conf)
        return cls.send_request(options)
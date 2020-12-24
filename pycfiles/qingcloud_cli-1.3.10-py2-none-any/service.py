# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/qs_client/actions/service.py
# Compiled at: 2016-02-29 09:00:15
from .base import BaseAction
from ...misc.utils import prints_body

class ListBucketsAction(BaseAction):
    command = 'list-buckets'
    usage = '%(prog)s [-z <zone> -f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-z', '--zone', dest='zone', help='On which zone to create the bucket')
        return parser

    @classmethod
    def send_request(cls, options):
        headers = {}
        if options.zone:
            headers['Location'] = options.zone
        resp = cls.conn.make_request('GET', headers=headers)
        prints_body(resp)
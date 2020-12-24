# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/qs_client/actions/multipart.py
# Compiled at: 2017-03-01 04:19:52
import os, sys, json
from .base import BaseAction
from ...misc.utils import prints_body
from ..constants import HTTP_OK_CREATED, HTTP_OK_NO_CONTENT

class InitiateMultipartAction(BaseAction):
    command = 'initiate-multipart'
    usage = '%(prog)s -b <bucket> -k <key> [-t <type> -z <zone> -f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-b', '--bucket', dest='bucket', required=True, help='The bucket name')
        parser.add_argument('-k', '--key', dest='key', help='The object name')
        parser.add_argument('-t', '--type', dest='type', default='application/octet-stream', help='The object type')
        return parser

    @classmethod
    def send_request(cls, options):
        headers = {}
        if options.type:
            headers['Content-Type'] = options.type
        params = {'uploads': None}
        resp = cls.conn.make_request('POST', options.bucket, options.key, headers=headers, params=params)
        prints_body(resp)
        return


class UploadMultipartAction(BaseAction):
    command = 'upload-multipart'
    usage = '%(prog)s -b <bucket> -k <key> -u <upload_id> -p <part_number> ' + '-d <data> [-z <zone> -f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-b', '--bucket', dest='bucket', required=True, help='The bucket name')
        parser.add_argument('-k', '--key', dest='key', required=True, help='The object name')
        parser.add_argument('-u', '--upload-id', dest='upload_id', required=True, help='ID for the initiated multipart upload')
        parser.add_argument('-p', '--part-number', dest='part_number', required=True, type=int, help='The number of this part')
        parser.add_argument('-F', '--file', dest='file', help='The object file')
        parser.add_argument('-d', '--data', dest='data', help='The object data')
        return parser

    @classmethod
    def send_request(cls, options):
        if options.file:
            if not os.path.isfile(options.file):
                print 'No such file: %s' % options.file
                sys.exit(-1)
            data = open(options.file, 'rb')
        elif options.data:
            data = options.data
        else:
            print 'Must specify --file or --data parameter'
            sys.exit(1)
        params = {'upload_id': options.upload_id, 
           'part_number': str(options.part_number)}
        resp = cls.conn.make_request('PUT', options.bucket, options.key, data=data, params=params)
        if resp.status != HTTP_OK_CREATED:
            prints_body(resp)


class ListMultipartAction(BaseAction):
    command = 'list-multipart'
    usage = '%(prog)s -b <bucket> -k <key> -u <upload_id> [-p <part_number_marker> ' + '-l <limit> -f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-b', '--bucket', dest='bucket', type=str, required=True, help='The bucket name')
        parser.add_argument('-k', '--key', dest='key', required=True, help='The object name')
        parser.add_argument('-u', '--upload-id', dest='upload_id', required=True, help='ID for the initiated multipart upload')
        parser.add_argument('-p', '--part-number-marker', dest='part_number_marker', type=int, help='The number to start with when listing multipart')
        parser.add_argument('-l', '--limit', dest='limit', type=int, default=20, help='The maximum number of parts returned')
        return parser

    @classmethod
    def send_request(cls, options):
        params = {'upload_id': options.upload_id}
        if options.part_number_marker is not None:
            params['part_number_marker'] = str(options.part_number_marker)
        if options.limit is not None:
            params['limit'] = str(options.limit)
        resp = cls.conn.make_request('GET', options.bucket, options.key, params=params)
        prints_body(resp)
        return


class CompleteMultipartAction(BaseAction):
    command = 'complete-multipart'
    usage = '%(prog)s -b <bucket> -k <key> -u <upload_id> -P <part_numbers> ' + '[-e <etag> -f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-b', '--bucket', dest='bucket', required=True, help='The bucket name')
        parser.add_argument('-k', '--key', dest='key', required=True, help='The object name')
        parser.add_argument('-u', '--upload-id', dest='upload_id', required=True, help='ID for the initiated multipart upload')
        parser.add_argument('-P', '--part-numbers', nargs='*', type=int, required=True, help='The object file')
        parser.add_argument('-e', '--etag', dest='etag', help='The checksum value of the object')
        return parser

    @classmethod
    def send_request(cls, options):
        params = {'upload_id': options.upload_id}
        parts = []
        for part_number in options.part_numbers:
            parts.append({'part_number': part_number})

        data = {'object_parts': parts}
        headers = {}
        if options.etag:
            headers['ETag'] = options.etag
        resp = cls.conn.make_request('POST', options.bucket, options.key, headers=headers, data=json.dumps(data), params=params)
        if resp.status != HTTP_OK_CREATED:
            prints_body(resp)


class AbortMultipartAction(BaseAction):
    command = 'abort-multipart'
    usage = '%(prog)s -b <bucket> -k <key> -u <upload_id> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-b', '--bucket', dest='bucket', required=True, help='The bucket name')
        parser.add_argument('-k', '--key', dest='key', required=True, help='The object name')
        parser.add_argument('-u', '--upload-id', dest='upload_id', required=True, help='ID for the initiated multipart upload')
        return parser

    @classmethod
    def send_request(cls, options):
        params = {'upload_id': options.upload_id}
        resp = cls.conn.make_request('DELETE', options.bucket, options.key, params=params)
        if resp.status != HTTP_OK_NO_CONTENT:
            prints_body(resp)
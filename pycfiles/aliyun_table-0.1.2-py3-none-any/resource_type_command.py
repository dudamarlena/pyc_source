# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /root/Documents/ros-cli/ros/resources/resource_type_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DescribeResourceTypesRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('resource-type', help='Returns types of resources')
    parser.add_argument('--status', help='The status of resource', choices=['UNKNOWN', 'SUPPORTED', 'DEPRECATED', 'UNSUPPORTED', 'HIDDEN'], default='SUPPORTED')
    parser.set_defaults(func=resource_type)


def resource_type(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeResourceTypesRequest.DescribeResourceTypesRequest()
    req.set_SupportStatus(args.status)
    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print jsonDumpsIndentStr
    else:
        for item in data.get('ResourceTypes'):
            print item
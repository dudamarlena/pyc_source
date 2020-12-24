# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /root/Documents/ros-cli/ros/resources/resource_type_detail_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DescribeResourceTypeDetailRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('resource-type-detail', help='Returns detail of the specific resource type')
    parser.add_argument('--name', help='The name of resource', required=True)
    parser.set_defaults(func=resource_type_detail)


def resource_type_detail(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeResourceTypeDetailRequest.DescribeResourceTypeDetailRequest()
    req.set_TypeName(args.name)
    return req


def print_response(data):
    jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    print jsonDumpsIndentStr
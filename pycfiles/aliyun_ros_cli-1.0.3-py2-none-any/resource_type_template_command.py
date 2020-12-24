# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Documents/ros-cli/ros/resources/resource_type_template_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DescribeResourceTypeTemplateRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('resource-type-template', help='Returns template of the specific resource type')
    parser.add_argument('--name', help='The name of resource', required=True)
    parser.set_defaults(func=resource_type_template)


def resource_type_template(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeResourceTypeTemplateRequest.DescribeResourceTypeTemplateRequest()
    req.set_TypeName(args.name)
    return req


def print_response(data):
    jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    print jsonDumpsIndentStr
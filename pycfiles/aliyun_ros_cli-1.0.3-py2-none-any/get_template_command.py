# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Documents/ros-cli/ros/templates/get_template_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DescribeTemplateRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('get-template', help='Returns the template body for a specified stack')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--stack-id', help='The id that is associated with the stack', required=True)
    parser.set_defaults(func=get_template)


def get_template(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeTemplateRequest.DescribeTemplateRequest()
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)
    return req


def print_response(data):
    jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    print jsonDumpsIndentStr
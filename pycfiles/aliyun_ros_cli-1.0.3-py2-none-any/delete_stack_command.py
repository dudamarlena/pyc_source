# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Documents/ros-cli/ros/stacks/delete_stack_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DeleteStackRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('delete-stack', help='Deletes the specified stack')
    parser.add_argument('--region-id', help='The region that is associated with the stack', required=True)
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--stack-id', help='The id that is associated with the stack', required=True)
    parser.set_defaults(func=delete_stack)


def delete_stack(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DeleteStackRequest.DeleteStackRequest()
    req.set_headers({'x-acs-region-id': args.region_id})
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)
    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print jsonDumpsIndentStr
    else:
        for k, v in data.items():
            print '%-20s:  %s' % (k, v)
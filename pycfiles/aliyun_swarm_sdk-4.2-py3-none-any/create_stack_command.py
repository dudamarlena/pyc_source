# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /root/Documents/ros-cli/ros/stacks/create_stack_command.py
# Compiled at: 2017-09-20 05:29:00
from aliyunsdkros.request.v20150901 import CreateStacksRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('create-stack', help='Creates a stack as specified in the template')
    parser.add_argument('--region-id', help='The region that is associated with the stack')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--template-url', help='Location of file containing the template body', required=True)
    parser.add_argument('--parameters', help='A list of Parameter structures that specify input parameters for the stack. Synatax: key=value,key=value')
    parser.add_argument('--disable-rollback', help='Set to true to disable rollback of the stack if stack creation failed', default=True, type=bool)
    parser.add_argument('--timeout-in-minutes', help='The amount of time that can pass before the stack status becomes CREATE_FAILED', default=60, type=int)
    parser.set_defaults(func=create_stack)


def create_stack(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = CreateStacksRequest.CreateStacksRequest()
    if args.region_id is not None:
        req.set_headers({'x-acs-region-id': args.region_id})
    else:
        req.set_headers({'x-acs-region-id': connect.REGION_ID})
    content = {}
    content['Name'] = args.stack_name
    file_context = utils.read_template(args.template_url)
    content['Template'] = file_context
    content['DisableRollback'] = args.disable_rollback
    content['TimeoutMins'] = args.timeout_in_minutes
    ps = {}
    if args.parameters is not None:
        s = args.parameters.split(',')
        for item in s:
            pair = item.split('=')
            ps[pair[0]] = pair[1]

    content['Parameters'] = ps
    jsonDumpsIndentStr = json.dumps(content, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    req.set_content(jsonDumpsIndentStr)
    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print jsonDumpsIndentStr
    else:
        for k, v in data.items():
            print '%-20s:  %s' % (k, v)
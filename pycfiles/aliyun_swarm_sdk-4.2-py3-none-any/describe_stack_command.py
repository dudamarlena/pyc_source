# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /root/Documents/ros-cli/ros/stacks/describe_stack_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DescribeStackDetailRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('describe-stack', help='Returns the description for the specified stack')
    parser.add_argument('--stack-name', help='The name that is associated with the stack', required=True)
    parser.add_argument('--stack-id', help='The id that is associated with the stack', required=True)
    parser.set_defaults(func=describe_stack)


def describe_stack(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeStackDetailRequest.DescribeStackDetailRequest()
    req.set_headers({'x-acs-region-id': connect.REGION_ID})
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)
    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print jsonDumpsIndentStr
    else:
        print '%-20s:  %s' % ('Name', data.get('Name'))
        print '%-20s:  %s' % ('Id', data.get('Id'))
        print '%-20s:  %s' % ('Description', data.get('Description'))
        print '%-20s:  %s' % ('Region', data.get('Region'))
        print '%-20s:  %s' % ('Status', data.get('Status'))
        print '%-20s:  %s' % ('StatusReason', data.get('StatusReason'))
        print '%-20s:  %s' % ('DisableRollback', data.get('DisableRollback'))
        print '%-20s:  %s' % ('TimeoutMins', data.get('TimeoutMins'))
        print '%-20s:  %s' % ('Created', data.get('Created'))
        print '%-20s:  %s' % ('Updated', data.get('Updated'))
        print '%-20s:  %s' % ('Webhook', data.get('Webhook'))
        print '\nParameters:'
        if data.get('Parameters') is not None:
            for k, v in data.get('Parameters').items():
                print '    %-20s: %s' % (k, v)

        print '\nOutputs:'
        if data.get('Outputs') is not None:
            for out in data.get('Outputs'):
                print '    %-20s: %s --- %s' % (out['OutputKey'], out['OutputValue'], out['Description'])

    return
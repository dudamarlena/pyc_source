# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Documents/ros-cli/ros/resources/list_resources_command.py
# Compiled at: 2017-08-09 04:01:30
from aliyunsdkros.request.v20150901 import DescribeResourcesRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('list-resources', help='Returns descriptions of all resources of the specified stack')
    parser.add_argument('--stack-name', help='The name of stack', required=True)
    parser.add_argument('--stack-id', help='The id of stack', required=True)
    parser.set_defaults(func=list_resources)


def list_resources(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = DescribeResourcesRequest.DescribeResourcesRequest()
    req.set_StackName(args.stack_name)
    req.set_StackId(args.stack_id)
    if args.region_id is not None:
        req.set_headers({'x-acs-region-id': args.region_id})
    else:
        req.set_headers({'x-acs-region-id': connect.REGION_ID})
    return req


def print_response(data):
    if connect.JSON_FORM:
        jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
        print jsonDumpsIndentStr
    else:
        for item in data:
            print '\n%-20s:  %s' % ('Id', item.get('Id'))
            print '%-20s:  %s' % ('Name', item.get('Name'))
            print '%-20s:  %s' % ('Type', item.get('Type'))
            print '%-20s:  %s' % ('Status', item.get('Status'))
            print '%-20s:  %s' % ('StatusReason', item.get('StatusReason'))
            print '%-20s:  %s' % ('ResourceData', item.get('ResourceData'))
            print '%-20s:  %s' % ('PhysicalId', item.get('PhysicalId'))
            print '%-20s:  %s' % ('Created', item.get('Created'))
            print '%-20s:  %s' % ('Updated', item.get('Updated'))
            print '%-20s:  %s\n' % ('Deleted', item.get('Deleted'))
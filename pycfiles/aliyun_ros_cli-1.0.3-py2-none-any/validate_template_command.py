# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Documents/ros-cli/ros/templates/validate_template_command.py
# Compiled at: 2017-09-25 05:26:43
from aliyunsdkros.request.v20150901 import ValidateTemplateRequest
import ros.apps.config as connect, ros.apps.utils as utils, json, os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def setup(subparsers):
    parser = subparsers.add_parser('validate-template', help='Validates a specified template')
    parser.add_argument('--template-url', help='Location of file containing the template body', required=True)
    parser.set_defaults(func=validate_template)


def validate_template(args):
    req = prepare_request(args)
    status, headers, body = utils.send_req(req)
    utils.deal_resp(status, headers, body, print_response)


def prepare_request(args):
    req = ValidateTemplateRequest.ValidateTemplateRequest()
    file_context = utils.read_template(args.template_url)
    req.set_content('{"Template":' + file_context + '}')
    return req


def print_response(data):
    print 'The template is ok:\n'
    jsonDumpsIndentStr = json.dumps(data, indent=connect.JSON_INDENT, ensure_ascii=False, sort_keys=True)
    print jsonDumpsIndentStr
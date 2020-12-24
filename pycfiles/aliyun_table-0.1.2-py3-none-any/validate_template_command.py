# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
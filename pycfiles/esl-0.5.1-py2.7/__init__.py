# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/esl/__init__.py
# Compiled at: 2016-04-16 03:23:53
import requests
from requests.status_codes import _codes
import sys
from eslyacc import parse
from eslast import *
from eslgenerator import ESLGenerator
from eslyacc import parse
from eslast import QueryStringNode, HeaderNode, BodyNode, ValueNode, ShellNode
from formatter import ColorFormatter
__version__ = '0.5.1'

def esl():
    _map = {'GET': requests.get, 
       'POST': requests.post, 
       'DELETE': requests.delete, 
       'PUT': requests.put}
    ast = parse((' ').join(sys.argv[1:]))
    if ast is not None:
        url = ast.left.url
        method = ast.method.name
        params = {}
        headers = {}
        body = {}
        for option in ast.right.options if ast.right else []:
            if isinstance(option.key, QueryStringNode):
                if isinstance(option.value, ValueNode):
                    params[option.key.key] = option.value.value
                elif isinstance(option.value, ShellNode):
                    params[option.key.key] = commands.getstatusoutput(option.value.value)[1]
            elif isinstance(option.key, HeaderNode):
                headers[option.key.key] = option.value.value
            elif isinstance(option.key, BodyNode):
                body[option.key.key] = option.value.value

        try:
            r = _map[method](url, data=body, params=params, headers=headers)
            cf = ColorFormatter()
            print '%d %s' % (r.status_code, _codes[r.status_code][0])
            for k, v in r.headers.iteritems():
                print cf.format_headers('%s: %s' % (k, v))

            print cf.format_body(r.text, r.headers.get('Content-Type', 'text/html'))
        except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
            print 'InvalidURL'

    return


def eslgo():
    ast = parse((' ').join(sys.argv[1:]))
    if ast is not None:
        generator = ESLGenerator(ast)
        print generator.to_go()
    return


def eslpython():
    ast = parse((' ').join(sys.argv[1:]))
    if ast is not None:
        generator = ESLGenerator(ast)
        print generator.to_python()
    return


def eslcurl():
    ast = parse((' ').join(sys.argv[1:]))
    if ast is not None:
        generator = ESLGenerator(ast)
        print generator.to_curl()
    return
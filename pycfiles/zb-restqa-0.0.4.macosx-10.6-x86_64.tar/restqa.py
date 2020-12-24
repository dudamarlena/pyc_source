# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ujnamss/anaconda2/lib/python2.7/site-packages/zb_restqa/restqa.py
# Compiled at: 2019-04-19 16:17:05
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
from builtins import object
import os, re, glob, yaml, jmespath, requests
JSON_SELECTOR_REGEX = b'(resp(\\.[a-zA-Z0-9]+)+)'

def none_function(ctxt):
    return ctxt


class RestTestsuiteDriver(object):

    def __init__(self, test_suite_dir, function_dict):
        self.test_suite_dir = test_suite_dir
        self.function_dict = function_dict

    def run_tests(self):
        test_suite_files_expr = (b'{}/*_test_suite.yml').format(self.test_suite_dir)
        suites = glob.glob(test_suite_files_expr)
        for suite in suites:
            with open(suite, b'r') as (yaml_in):
                suite_settings = yaml.safe_load(yaml_in)
                suite_settings = suite_settings[b'suite']
                suite_base_url = suite_settings.get(b'base_url', None)
                print((b'suite_base_url: {}').format(suite_base_url))
                suite_name = suite_settings.get(b'name', None)
                suite_setup = suite_settings.get(b'setup', None)
                suite_teardown = suite_settings.get(b'teardown', None)
                print((b'suite: {}::setup_function: {}::teardown_function: {}').format(suite_name, suite_setup, suite_teardown))
                try:
                    ctxt = {}
                    setup_function = self.function_dict.get(suite_setup, none_function)
                    ctxt = setup_function(ctxt)
                    tests = suite_settings.get(b'tests', [])
                    for test_settings in tests:
                        try:
                            test_name = test_settings.get(b'name', b'None')
                            test_json_payload = test_settings.get(b'json', False)
                            test_http_headers = test_settings.get(b'headers', [])
                            test_http_method = test_settings.get(b'method', b'GET')
                            test_http_path = test_settings.get(b'path', None)
                            test_http_payload = test_settings.get(b'payload', None)
                            test_pre = test_settings.get(b'pre_test', None)
                            test_post = test_settings.get(b'post_test', None)
                            test_assertions = test_settings.get(b'assertions', None)
                            headers = {}
                            for test_http_header in test_http_headers:
                                for header_name, header_value in test_http_header.items():
                                    headers[header_name] = header_value

                            optional_params = {b'headers': headers}
                            if test_http_method == b'GET' and test_http_payload != None:
                                optional_params[b'params'] = test_http_payload
                            if test_http_method == b'POST':
                                if test_http_payload != None:
                                    if test_json_payload:
                                        optional_params[b'json'] = json.dumps(test_http_payload)
                                    else:
                                        optional_params[b'data'] = test_http_payload
                            request_url = (b'{}{}').format(suite_base_url, test_http_path)
                            print((b'request_url: {}').format(request_url))
                            test_pre_function = self.function_dict.get(test_pre, none_function)
                            ctxt = test_pre_function(ctxt)
                            try:
                                resp = requests.request(test_http_method, request_url, **optional_params)
                                resp = resp.json()
                                locals = {b'ctxt': ctxt, 
                                   b'resp': resp}
                                for expression in test_assertions:
                                    matches = re.findall(JSON_SELECTOR_REGEX, expression)
                                    print((b'expression: {}/properties: {}').format(expression, matches))
                                    for match in matches:
                                        replace_expr = match[0].replace(b'resp\\.', b'')
                                        replace_expr = (b"{}'{}'{}").format(b'jmespath.search(', replace_expr, b', resp)')
                                        expression = expression.replace(match[0], replace_expr)

                                    print((b'New expression: {}').format(expression))
                                    eval(expression, None, locals)

                            except Exception as e2:
                                print((b'Exception occured while executing suite: {} / test: {} / {}').format(suite_name, test_name, e2))

                            test_post_function = self.function_dict.get(test_post, none_function)
                            ctxt = test_post_function(ctxt)
                        except Exception as e1:
                            print((b'Exception occured while executing suite: {} / test: {} / {}').format(suite_name, test_name, e1))

                    teardown_function = self.function_dict.get(suite_teardown, none_function)
                    ctxt = teardown_function(ctxt)
                except Exception as e:
                    print((b'Exception occured while executing test suite: {}/{}').format(suite_name, e))

        return
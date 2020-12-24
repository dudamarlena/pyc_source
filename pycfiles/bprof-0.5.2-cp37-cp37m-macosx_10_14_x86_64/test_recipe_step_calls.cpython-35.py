# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/tests/test_recipe_step_calls.py
# Compiled at: 2016-08-21 10:12:43
# Size of source mod 2**32: 19617 bytes
__doc__ = '\nTO TEST:\n [x] error handling with bad URL\n [x] http-codes (check for different numbers) \n [x] missing content-type response header aborts unless a 204 & 205 response code is returned\n [x] error handling with socket/timeout error\n [ ] error handling with ssl ignoring - NOT TESTED (YET)\n\n [x] setting of request explicit headers\n [x] bad options passed (type, or unrecognised key or value)\n [x] default request headers set okay (host, user-agent, others)\n [x] http method types (including weird ones) -- Note, unknown methods deliberately passed through\n [x] http retries -- MANUALLY TESTED ONLY (eyeball)\n [ ] http request body (json and URL encode)\n [x] retry after 4xx or 5xx (option passed)\n\n'
import sys
sys.path.append('/home/travis/build/bradwood/BPRC/bprc')
sys.path.append('/home/travis/build/bradwood/BPRC/bprc/tests')
print(sys.path)
import unittest
from mock import Mock
from mock import MagicMock
import yaml, requests, requests_mock
from ddt import ddt, data, file_data, unpack
from bprc.recipe import Recipe
from bprc.stepprocessor import StepProcessor
from bprc.varprocessor import VarProcessor
from bprc.variables import Variables
from bprc.utils import *
from bprc._version import __version__

@ddt
class SimpleTest(unittest.TestCase):

    def setUp(self):
        """Sets up the YAML data."""
        with open('tests/yaml_call_test.yml', 'r') as (myfile):
            self.yamldata = myfile.read()
        datamap = yaml.load(self.yamldata)
        self.r = Recipe(datamap)

    @data(0, 1, 2, 3, 5, 6, 7, 8)
    @requests_mock.Mocker(kw='mock')
    def test_bad_URLs(self, id, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(requests_mock.GET, requests_mock.ANY, status_code=200, headers={'content-type': 'application/json'}, json={'msg': 'hello'})
        with self.assertRaises(ValueError):
            prepared_statement = processor.call()

    @unpack
    @data([
     9,
     200,
     requests_mock.GET,
     'http://two.com',
     {'someheader': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_server_sent_no_content_header(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        with self.assertRaises(KeyError):
            prepared_statement = processor.call()

    @unpack
    @data([
     9,
     204,
     requests_mock.GET,
     'http://two.com',
     {'someheader': 'application/json'},
     {'msg': 'hello'}], [
     9,
     205,
     requests_mock.GET,
     'http://two.com',
     {'someheader': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_server_sent_no_content_header_ok_for_204_or_205(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        prepared_statement = processor.call()
        self.assertEqual(self.r.steps[id].response.code, code)
        self.assertEqual(self.r.steps[id].response.headers, headers)

    @unpack
    @data([
     9,
     200,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_basic_call(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        prepared_statement = processor.call()
        self.assertEqual(self.r.steps[id].response.code, 200)

    def _connection_error(self):
        raise requests.exceptions.ConnectionError

    def _ssl_error(self):
        raise requests.exceptions.SSLError

    @unpack
    @data([
     9,
     200,
     requests_mock.GET,
     'http://two.com',
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    def test_connection_error(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        requests.send = MagicMock(side_effect=self._connection_error)
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        with self.assertRaises(requests.exceptions.ConnectionError) as (cm):
            prepared_statement = processor.call()

    @unpack
    @data([
     11,
     200,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test__bad_options_passed(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        """checks if type checks are done on request.retries"""
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        with self.assertRaises(ValueError):
            prepared_statement = processor.call()

    @unpack
    @data([
     12,
     200,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_default_passed(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        """checks if type checks are done on request.retries"""
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)

    @unpack
    @data([
     13,
     200,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_default_headers_set(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        prepared_statement = processor.call()
        self.assertEqual(self.r.steps[id].request.headers['user-agent'], 'bprc/' + __version__)
        self.assertEqual(self.r.steps[id].request.headers['host'], 'this.is.a.url.org')

    @unpack
    @data([
     14,
     200,
     requests_mock.POST,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     200,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     16,
     200,
     requests_mock.DELETE,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     17,
     200,
     requests_mock.PUT,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     18,
     200,
     requests_mock.PATCH,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     19,
     200,
     requests_mock.HEAD,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     20,
     200,
     requests_mock.OPTIONS,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_default_http_methods(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        prepared_statement = processor.call()
        self.assertEqual(self.r.steps[id].httpmethod, method)

    @unpack
    @data([
     15,
     200,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     14,
     201,
     requests_mock.POST,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     206,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_non_error_http_response_codes(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        prepared_statement = processor.call()
        self.assertEqual(self.r.steps[id].response.code, code)

    @unpack
    @data([
     15,
     401,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     404,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     500,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     410,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_error_http_response_codes(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        with self.assertRaises(requests.exceptions.HTTPError):
            prepared_statement = processor.call()

    @unpack
    @data([
     15,
     401,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     404,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     500,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}], [
     15,
     410,
     requests_mock.GET,
     requests_mock.ANY,
     {'content-type': 'application/json'},
     {'msg': 'hello'}])
    @requests_mock.Mocker(kw='mock')
    def test_error_http_response_codes_suppressed(self, id, code, method, urlmatch, headers, json_body, **kwargs):
        processor = StepProcessor(recipe=self.r, stepid=id, variables={})
        self.r.steps[id] = processor.prepare()
        kwargs['mock'].request(method, urlmatch, status_code=code, headers=headers, json=json_body)
        import bprc.cli
        bprc.cli.args = bprc.cli.parser.parse_args(['--skip-http-errors'])
        prepared_statement = processor.call()
        self.assertEqual(self.r.steps[id].response.code, code)


if __name__ == '__main__':
    unittest.main()
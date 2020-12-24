# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/PoorHttp/PoorWSGI/examples/openapi3.py
# Compiled at: 2020-02-05 15:58:26
# Size of source mod 2**32: 3293 bytes
from wsgiref.simple_server import make_server
from os import urandom, path
from sys import path as python_path
import logging as log, json
from openapi_core import create_spec
from openapi_core.shortcuts import RequestValidator, ResponseValidator
from openapi_core.schema.operations.exceptions import InvalidOperation
from openapi_core.schema.servers.exceptions import InvalidServer
from openapi_core.schema.paths.exceptions import InvalidPath
TEST_PATH = path.dirname(__file__)
python_path.insert(0, path.abspath(path.join(TEST_PATH, path.pardir)))
from poorwsgi import Application, state
from poorwsgi.response import Response, abort
from poorwsgi.openapi_wrapper import OpenAPIRequest, OpenAPIResponse
app = application = Application('OpenAPI3 Test App')
app.debug = True
app.secret_key = urandom(32)
request_validator = None
response_validator = None
with open(path.join(path.dirname(__file__), 'openapi.json'), 'r') as (openapi):
    spec = create_spec(json.load(openapi))
    request_validator = RequestValidator(spec)
    response_validator = ResponseValidator(spec)

@app.before_request()
def before_each_request(req):
    req.api = OpenAPIRequest(req)
    result = request_validator.validate(req.api)
    if result.errors:
        errors = []
        for error in result.errors:
            if isinstance(error, (InvalidOperation, InvalidServer,
             InvalidPath)):
                log.debug(error)
                return
            errors.append(repr(error) + ':' + str(error))

        abort(Response((json.dumps({'error': ';'.join(errors)})), status_code=400,
          content_type='application/json'))


@app.after_request()
def after_each_request(req, res):
    """Check if ansewer is valid by OpenAPI."""
    result = response_validator.validate(req.api or OpenAPIRequest(req), OpenAPIResponse(res))
    for error in result.errors:
        if isinstance(error, InvalidOperation):
            pass
        else:
            log.error('API output error: %s', str(error))

    return res


@app.route('/plain_text')
def plain_text(req):
    return ('Hello world', 'text/plain')


@app.route('/json/<arg>')
def ajax_arg(req, arg):
    return (
     json.dumps({'arg': arg}), 'application/json')


@app.route('/arg/<int_arg:int>')
def ajax_integer(req, arg):
    return (
     json.dumps({'integer_arg': arg}), 'application/json')


@app.route('/arg/<float_arg:float>')
def ajax_float(req, arg):
    return (
     json.dumps({'float_arg': arg}), 'application/json')


@app.route('/internal-server-error')
def method_raises_errror(req):
    raise RuntimeError('Test of internal server error')


@app.http_state(state.HTTP_NOT_FOUND)
def not_found(req):
    return (
     json.dumps({'error': 'Url %s, you are request not found' % req.uri}),
     'application/json', None, 404)


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8080, app)
    httpd.serve_forever()
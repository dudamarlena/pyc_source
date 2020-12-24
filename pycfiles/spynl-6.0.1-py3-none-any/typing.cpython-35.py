# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/serial/typing.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 3248 bytes
"""
Deal with content types in a generic way. Negotiate incoming content types.
"""
from mimetypes import guess_type
from spynl.main.serial import xml, json, py, html, yaml, csv
from spynl.main.serial.exceptions import UndeterminedContentTypeException
from spynl.main.serial.exceptions import UnsupportedContentTypeException
handlers = {'application/json': {'dump': json.dumps, 
                      'load': json.loads, 
                      'sniff': json.sniff}, 
 
 'application/xml': {'dump': xml.dumps, 
                     'load': xml.loads, 
                     'sniff': xml.sniff}, 
 
 'application/x-yaml': {'dump': yaml.dumps, 
                        'load': yaml.loads, 
                        'sniff': yaml.sniff}, 
 
 'text/csv': {'dump': csv.dumps, 
              'load': csv.loads, 
              'sniff': csv.sniff}, 
 
 'text/html': {'dump': html.dumps}, 
 'text/x-python': {'dump': py.dumps}}
handlers['text/xml'] = handlers['application/xml']

def negotiate_request_content_type(request):
    """
    Negotiate and return a content type for this request.
    Priorisation:
    1. Content-Type Header
    2. Body sniffing
    Throw an Exception when can't find a type (but have a body) or
    if we end up with a type we don't know
    (but the request method is POST|PUT).
    """
    content_type = request.content_type
    if not content_type or content_type not in handlers:
        for key, values in handlers.items():
            if 'sniff' in values and values['sniff'](request.text):
                return key

    if not content_type:
        if not request.body:
            return
        raise UndeterminedContentTypeException()
    if content_type not in handlers and request.method in ('POST', 'PUT'):
        raise UnsupportedContentTypeException(content_type)
    return content_type


def negotiate_response_content_type(request):
    """
    Negotiate and return a content type to be used in the response.

    Priorisation:
    1. file extension in the URL
    2. Accept Header (only first mentioned type)
    3. Originally set Content-Type (e.g. browser default or set by a view)
    4. Spynl default (application/json)
    """
    content_type = None
    if hasattr(request, 'path_extension') and request.path_extension:
        content_type = request.path_extension
    accept_type = None
    if 'Accept' in request.headers:
        accept_type = request.headers['Accept'].split(',')[0]
    if not content_type and accept_type and accept_type not in ('text/html', '*/*'):
        content_type = accept_type
    if not content_type:
        content_type = request.response.content_type
    if not content_type:
        content_type = 'application/json'
    if content_type and '/' not in content_type:
        content_type = guess_type('file.' + content_type)[0]
    return content_type


def supported_types():
    """Return the types supported for serialisation"""
    return list(handlers.keys())
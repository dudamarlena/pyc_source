# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/util.py
# Compiled at: 2017-09-29 12:38:41
# Size of source mod 2**32: 3208 bytes
"""
Misc utilities for usage inside the framework.
"""
import json, typing
from werkzeug.wrappers import Response

def as_html(text: str, code: int=200, headers: dict=None) -> Response:
    """
    Returns a HTML response.
    
    .. code-block:: python
    
        return as_html("<h1>Hel Na</h1>", code=403)
    
    :param text: The text to return. 
    :param code: The status code of the response.
    :param headers: Any optional headers.
    :return: A new :class:`werkzeug.wrappers.Response` representing the HTML. 
    """
    if headers is None:
        headers = {}
    r = Response(text, status=code, headers={**{'Content-Type': 'text/html'}, **headers})
    return r


def as_plaintext(text: str, code: int=200, headers: dict=None) -> Response:
    """
    Returns a plaintext response.
    
    .. code-block:: python
    
        return as_plaintext("hel yea", code=201)
    
    :param text: The text to return. 
    :param code: The status code of the response.
    :param headers: Any optional headers.
    :return: A new :class:`werkzeug.wrappers.Response` representing the text.
    """
    if headers is None:
        headers = {}
    r = Response(text, status=code, headers={**{'Content-Type': 'text/plain'}, **headers})
    return r


def as_json(data: typing.Union[(dict, list)], code: int=200, headers: dict=None, *, json_encoder: json.JSONEncoder=None, **kwargs) -> Response:
    """
    Returns a JSON response.
    
    .. code-block:: python
    
        return as_json({"response": "yes", "code": 201}, code=201)
    
    :param data: The data to encode.
    :param code: The status code of the response.
    :param headers: Any optional headers.
    :param json_encoder: The encoder class to use to encode.
    :return: A new :class:`werkzeug.wrappers.Response` representing the JSON.
    """
    if headers is None:
        headers = {}
    dumped = (json.dumps)(data, cls=json_encoder, **kwargs)
    r = Response(dumped, status=code, headers=headers)
    return r


def wrap_response(args, response_class: Response=Response) -> Response:
    """
    Wrap up a response, if applicable.
    This allows Flask-like `return "whatever"`.

    :param args: The arguments that are being wrapped.
    :param response_class: The Response class that is being used.
    """
    if not args:
        return response_class('', status=204)
    else:
        if isinstance(args, tuple):
            if len(args) == 1:
                return response_class((args[0]), status=200)
            else:
                if len(args) == 2:
                    return response_class((args[0]), status=(args[1]))
                if len(args) == 3:
                    return response_class((args[0]), status=(args[1]), headers=(args[2]))
            raise TypeError('Cannot return more than 3 arguments from a view')
        if isinstance(args, response_class):
            return args
        return response_class(args)
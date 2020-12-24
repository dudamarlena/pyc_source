# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/__init__.py
# Compiled at: 2017-09-29 12:38:41
# Size of source mod 2**32: 1249 bytes
"""
Kyoukai is an async web framework for Python 3.5 and above.

.. currentmodule:: kyoukai

.. autosummary::
    :toctree: Kyoukai
        
    app
    backends
    asphalt
    blueprint
    route
    routegroup
    testing
    util
"""
import json
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.formparser import FormDataParser

def _parse_json(parser: FormDataParser, stream, mimetype, content_length, options):
    if parser.max_content_length is not None:
        if content_length is not None:
            if content_length > parser.max_content_length:
                raise RequestEntityTooLarge()
    data = stream.read().decode()
    return (stream, json.loads(data), {})


FormDataParser.parse_functions['application/json'] = _parse_json
from kyoukai.app import Kyoukai, __version__
from kyoukai.asphalt import HTTPRequestContext, KyoukaiComponent
from kyoukai.blueprint import Blueprint
from kyoukai.route import Route
from kyoukai.routegroup import RouteGroup
from kyoukai.testing import TestKyoukai
__all__ = ('Kyoukai', 'HTTPRequestContext', 'KyoukaiComponent', 'Blueprint', 'Route',
           'RouteGroup', 'TestKyoukai')
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/server/responses.py
# Compiled at: 2016-03-03 11:26:31
# Size of source mod 2**32: 812 bytes
import json
from typing import Optional, Any, List, Dict, TypeVar
from aiohttp import web
JsonApiPayload = TypeVar('JsonApiPayload', Dict[(str, Any)], List[Dict[(str, Any)]])

def ok(data: Optional[JsonApiPayload]=None) -> web.Response:
    if data is None:
        data = {}
    return _response(200, data)


def _response(status: int, data: JsonApiPayload) -> web.Response:
    """ Generate a final response in JSON API format:

    * http://jsonapi.org/format/#document-top-level
    * http://jsonapi.org/format/#document-resource-identifier-objects
    """
    data = {'data': data, 
     'jsonapi': {'version': '1.0'}}
    return web.Response(status=status, text=json.dumps(data), content_type='application/vnd.api+json')
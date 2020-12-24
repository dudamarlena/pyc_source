# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/route_api/avishan/middlewares.py
# Compiled at: 2020-02-26 07:06:26
# Size of source mod 2**32: 1168 bytes
import json, falcon
from avishan.utils import json_serializer

class JSONTranslator:

    def process_request(self, req, resp):
        """
        req.stream corresponds to the WSGI wsgi.input environ variable,
        and allows you to read bytes from the request body.
        See also: PEP 3333
        """
        if req.content_length in (None, 0):
            return
            body = req.bounded_stream.read()
            if not body:
                raise falcon.HTTPBadRequest('Empty request body. A valid JSON document is required.')
        else:
            try:
                req.context['request'] = json.loads(body.decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                raise falcon.HTTPError(falcon.HTTP_753, 'Malformed JSON. Could not decode the request body.The JSON was incorrect or not encoded as UTF-8.')

    def process_response(self, req, resp, resource, req_succeeded):
        if 'response' not in resp.context:
            return
        resp.body = json.dumps((resp.context['response']),
          default=json_serializer)
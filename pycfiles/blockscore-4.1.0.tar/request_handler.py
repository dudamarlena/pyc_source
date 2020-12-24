# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/http_client/request_handler.py
# Compiled at: 2015-03-04 21:31:22
import json

class RequestHandler:

    @staticmethod
    def renderKey(parents):
        depth, new = (0, '')
        for x in parents:
            old = '[%s]' if depth > 0 else '%s'
            new += old % x
            depth += 1

        return new

    @staticmethod
    def urlencode(data, parents=None, pairs=None):
        if pairs is None:
            pairs = {}
        if parents is None:
            parents = []
        if isinstance(data, dict):
            for key, value in data.items():
                RequestHandler.urlencode(value, parents + [key], pairs)

        elif isinstance(data, list):
            for key, value in enumerate(data):
                RequestHandler.urlencode(value, parents + [key], pairs)

        else:
            pairs[RequestHandler.renderKey(parents)] = data
        return pairs

    @staticmethod
    def set_body(request):
        typ = request['request_type'] if 'request_type' in request else 'form'
        if typ == 'json':
            request['data'] = json.dumps(request['data'])
            request['headers']['content-type'] = 'application/json'
        if typ == 'form':
            request['data'] = RequestHandler.urlencode(request['data'])
            request['headers']['content-type'] = 'application/x-www-form-urlencoded'
        if typ == 'raw':
            if 'content-type' in request['headers']:
                del request['headers']['content-type']
        if 'request_type' in request:
            del request['request_type']
        return request
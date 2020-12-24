# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/shanedasilva/src/ghc/coinbase/coinbase-python/tests/helpers.py
# Compiled at: 2018-01-17 19:23:46
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json, re, six, httpretty as hp

def mock_response(method, uri, data, errors=None, warnings=None, pagination=None):

    def wrapper(fn):

        @six.wraps(fn)
        @hp.activate
        def inner(*args, **kwargs):
            body = {b'data': data}
            if errors is not None:
                body[b'errors'] = errors
            if warnings is not None:
                body[b'warnings'] = warnings
            if pagination is not None:
                body[b'pagination'] = pagination
            hp.reset()
            hp.register_uri(method, re.compile(b'.*' + uri + b'$'), json.dumps(body))
            return fn(*args, **kwargs)

        return inner

    return wrapper
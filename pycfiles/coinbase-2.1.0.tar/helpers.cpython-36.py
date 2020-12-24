# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shanedasilva/src/ghc/coinbase/coinbase-python/tests/helpers.py
# Compiled at: 2018-01-17 19:23:46
# Size of source mod 2**32: 782 bytes
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
            body = {'data': data}
            if errors is not None:
                body['errors'] = errors
            if warnings is not None:
                body['warnings'] = warnings
            if pagination is not None:
                body['pagination'] = pagination
            hp.reset()
            hp.register_uri(method, re.compile('.*' + uri + '$'), json.dumps(body))
            return fn(*args, **kwargs)

        return inner

    return wrapper
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/services/credentials_service.py
# Compiled at: 2020-05-06 01:54:06
# Size of source mod 2**32: 802 bytes
from __future__ import absolute_import, division, print_function
import json, requests

def fetch_credentials(config):
    response = _get_requests().get((config.get_uri_context() + '/accounts/streaming-credentials'), headers=(config.get_headers()))
    if response.status_code == 401:
        msg = 'Extraction API authentication failed for given credentials header:\n            {0}'.format(config.headers)
        raise Exception(msg)
    try:
        streaming_credentials_string = json.loads(response.text)['data']['attributes']['streaming_credentials']
    except KeyError:
        raise Exception('Unable to find streaming credentials for given account')

    return json.loads(streaming_credentials_string)


def _get_requests():
    return requests
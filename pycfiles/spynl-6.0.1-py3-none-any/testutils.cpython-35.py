# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/testutils.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 1354 bytes
"""Helper functions for tests to use."""
import json

def post(application, view, params=None, content_type='application/json', expect_errors=False, return_headers=False):
    """
    Make a POST request and get a json object back.

    Helper method to save typing.
    """
    if params is None:
        params = {}
    if 'json' in content_type:
        paramstr = json.dumps(params)
    response = application.post(view, params=paramstr, headers={'Content-Type': content_type}, expect_errors=expect_errors)
    if response.text:
        rtext = json.loads(response.text)
        if return_headers:
            return (rtext, response.headers)
        return rtext
    if return_headers:
        return response.headers


def get(application, path, expect_errors=False, return_headers=False, headers=None):
    """
    Make a GET request and get a json object back.

    Helper method to save typing.
    """
    response = application.get(path, expect_errors=expect_errors, headers=headers)
    if response.text:
        rtext = json.loads(response.text)
        if return_headers:
            return (rtext, response.headers)
        return rtext
    if return_headers:
        return response.headers
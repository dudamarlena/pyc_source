# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/attrdict.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 692 bytes
from eth_utils import is_dict
from web3.utils.datastructures import AttributeDict
from web3.utils.toolz import assoc

def attrdict_middleware(make_request, web3):
    """
    Converts any result which is a dictionary into an a
    """

    def middleware(method, params):
        response = make_request(method, params)
        if 'result' in response:
            result = response['result']
            if is_dict(result):
                if not isinstance(result, AttributeDict):
                    return assoc(response, 'result', AttributeDict.recursive(result))
            return response
        else:
            return response

    return middleware
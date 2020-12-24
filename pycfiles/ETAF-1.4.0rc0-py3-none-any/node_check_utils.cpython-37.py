# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/utils/node_check_utils.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2273 bytes
import functools, requests
from flask import request
from fate_flow.settings import CHECK_NODES_IDENTITY, MANAGER_HOST, MANAGER_PORT, FATE_MANAGER_NODE_CHECK

def check_nodes(func):

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        if CHECK_NODES_IDENTITY:
            body = {'partyId':request.json.get('src_party_id'),  'role':request.json.get('src_role'), 
             'appKey':request.json.get('appKey'), 
             'appSecret':request.json.get('appSecret')}
            try:
                response = requests.post(url=('http://{}:{}{}'.format(MANAGER_HOST, MANAGER_PORT, FATE_MANAGER_NODE_CHECK)), json=body).json()
                if response['code'] != 0:
                    raise Exception('Authentication failure: {}'.format(str(response['message'])))
            except Exception as e:
                try:
                    raise Exception('Authentication error: {}'.format(str(e)))
                finally:
                    e = None
                    del e

        return func(*args, **kwargs)

    return _wrapper


def nodes_check(src_party_id, src_role, appKey, appSecret):
    if CHECK_NODES_IDENTITY:
        body = {'partyId':src_party_id,  'role':src_role, 
         'appKey':appKey, 
         'appSecret':appSecret}
        try:
            response = requests.post(url=('http://{}:{}{}'.format(MANAGER_HOST, MANAGER_PORT, FATE_MANAGER_NODE_CHECK)), json=body).json()
            if response['code'] != 0:
                raise Exception(str(response['message']))
        except Exception as e:
            try:
                raise Exception('role {} party id {} Authentication error: {}'.format(src_role, src_party_id, str(e)))
            finally:
                e = None
                del e
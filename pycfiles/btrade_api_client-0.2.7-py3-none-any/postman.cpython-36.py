# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/btp/util/postman.py
# Compiled at: 2017-11-04 01:43:23
# Size of source mod 2**32: 775 bytes
import uuid, requests
from btp.util import req

def __build_post_body(token, url_list):
    return {'jsonrpc':'2.0', 
     'method':'aria2.changeGlobalOption', 
     'id':str(uuid.uuid4()), 
     'params':[
      'token:{token}'.format(token=token),
      {'bt-tracker': ','.join(url_list)}]}


def push(aria2_jsonrpc_url, aria2_jsonrpc_token, url_list, proxy=None):
    post_body = __build_post_body(aria2_jsonrpc_token, url_list)
    resp = requests.post(aria2_jsonrpc_url, json=post_body, proxies=(req.build_proxies(proxy))).json()
    if resp:
        if 'result' in resp:
            if resp['result'] == 'OK':
                return True
    return False
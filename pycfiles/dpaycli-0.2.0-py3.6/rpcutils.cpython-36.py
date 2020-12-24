# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycliapi/rpcutils.py
# Compiled at: 2018-10-15 03:14:05
# Size of source mod 2**32: 2886 bytes
"""graphennewsrpc."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import time, json, logging
from .exceptions import UnauthorizedError, RPCConnection, RPCError, NumRetriesReached, CallRetriesReached
from .node import Nodes
log = logging.getLogger(__name__)

def is_network_appbase_ready(props):
    """Checks if the network is appbase ready"""
    if 'DPAY_BLOCKCHAIN_VERSION' in props:
        return False
    if 'DPAY_BLOCKCHAIN_VERSION' in props:
        return True


def get_query(appbase, request_id, api_name, name, args):
    query = []
    if not appbase or api_name == 'condenser_api':
        query = {'method':'call', 
         'params':[
          api_name, name, list(args)], 
         'jsonrpc':'2.0', 
         'id':request_id}
    else:
        args = json.loads(json.dumps(args))
    if len(args) > 0 and isinstance(args, list) and isinstance(args[0], dict):
        query = {'method':api_name + '.' + name, 
         'params':args[0], 
         'jsonrpc':'2.0', 
         'id':request_id}
    elif len(args) > 0 and isinstance(args, list) and isinstance(args[0], list) and len(args[0]) > 0 and isinstance(args[0][0], dict):
        for a in args[0]:
            query.append({'method':api_name + '.' + name,  'params':a, 
             'jsonrpc':'2.0', 
             'id':request_id})
            request_id += 1

    else:
        if args:
            query = {'method':'call', 
             'params':[
              api_name, name, list(args)], 
             'jsonrpc':'2.0', 
             'id':request_id}
            request_id += 1
        else:
            if api_name == 'condenser_api':
                query = {'method':api_name + '.' + name, 
                 'jsonrpc':'2.0', 
                 'params':[],  'id':request_id}
            else:
                query = {'method':api_name + '.' + name, 
                 'jsonrpc':'2.0', 
                 'params':{},  'id':request_id}
    return query


def get_api_name(appbase, *args, **kwargs):
    if not appbase:
        if 'api' in kwargs:
            if len(kwargs['api']) > 0:
                api_name = kwargs['api'].replace('_api', '') + '_api'
        api_name = None
    elif 'api' in kwargs:
        if len(kwargs['api']) > 0:
            if kwargs['api'] not in ('jsonrpc', 'hive'):
                api_name = kwargs['api'].replace('_api', '') + '_api'
            else:
                api_name = kwargs['api']
    else:
        api_name = 'condenser_api'
    return api_name
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/api_utils.py
# Compiled at: 2015-02-12 15:25:14
import requests, json
global_id = 0

def create_message(method_name, params, id):
    id += 1
    message = {'jsonrpc': '2.0', 
       'method': method_name, 
       'params': params, 
       'id': str(id)}
    json_message = json.dumps(message)
    return (json_message, id)


def call(method_name, args_dict, URI, id=None, print_message=False):
    global global_id
    if id is None:
        id = global_id
    message, id = create_message(method_name, args_dict, id)
    global_id = global_id + 1
    if print_message:
        print 'trying message:', message
    r = requests.put(URI, data=message)
    r.raise_for_status()
    out = json.loads(r.content)
    if isinstance(out, dict) and 'result' in out:
        out = out['result']
    else:
        print 'call(%s, <args_dict>, %s): ERROR' % (method_name, URI)
    return (
     out, id)


def call_and_print(method_name, args_dict, URI, id=0):
    out, id = call(method_name, args_dict, URI, id=id, print_message=True)
    print out
    print
    return (out, id)
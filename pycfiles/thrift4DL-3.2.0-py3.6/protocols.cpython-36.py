# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/tcp/protocols.py
# Compiled at: 2020-01-12 21:21:44
# Size of source mod 2**32: 356 bytes
import json

def cvt_vision_result_proto(error_code, error_message, content):
    json_data = {'error_code':error_code, 
     'error_message':error_message, 
     'content':content}
    return json.dumps(json_data)
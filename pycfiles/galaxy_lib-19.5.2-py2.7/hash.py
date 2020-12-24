# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/hash.py
# Compiled at: 2018-04-20 03:19:42
import hashlib, json

def build_tool_hash(as_dict):
    as_str = json.dumps(as_dict, sort_keys=True)
    m = hashlib.sha256()
    m.update(as_str)
    hash = m.hexdigest()
    return hash
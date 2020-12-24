# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrestful/converttype.py
# Compiled at: 2019-03-17 21:04:35
# Size of source mod 2**32: 408 bytes
import json
from collections import namedtuple

def json2object(doc, name=None):
    if not isinstance(doc, dict):
        return
    if name == None:
        name = doc.keys()
    data = json.dumps(doc)
    return json.loads(data, object_hook=(lambda d: (namedtuple(name, d.keys()))(*d.values())))


def object2json(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return
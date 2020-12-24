# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/lib/utils.py
# Compiled at: 2017-12-22 12:35:42
import json
from future.utils import iteritems

def dump_json(obj):
    return json.dumps(obj, indent=2, separators=(',', ': '), default=lambda o: dict((k, v) for k, v in iteritems(o.__dict__) if v is not None))


def im_func(obj):
    if hasattr(obj, 'im_func'):
        return getattr(obj, 'im_func')
    if hasattr(obj, '__func__'):
        return getattr(obj, '__func__')


def im_self(obj):
    if hasattr(obj, 'im_self'):
        return getattr(obj, 'im_self')
    if hasattr(obj, '__self__'):
        return getattr(obj, '__self__')
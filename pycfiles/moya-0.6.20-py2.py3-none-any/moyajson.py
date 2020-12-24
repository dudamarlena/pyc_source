# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/moyajson.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import absolute_import
import json

class _MoyaEncoder(json.JSONEncoder):
    """A customer encoder for Moya objects"""

    def default(self, obj):
        if hasattr(obj, '__moyajson__'):
            return obj.__moyajson__()
        return super(_MoyaEncoder, self).default(obj)


def dumps(obj, *args, **kwargs):
    """Allows objects to define how they are serialized to JSON,
    if an object contains a '__moyajson__' method, that will be called and the
    result will be encoded rather than the instance"""
    return json.dumps(obj, cls=_MoyaEncoder, *args, **kwargs)


loads = json.loads
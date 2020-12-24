# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/dispatch/resource/helper.py
# Compiled at: 2019-06-10 13:47:18
# Size of source mod 2**32: 421 bytes
"""Helpers for advanced controller behaviour.

Much work needs to be done.
"""
from functools import partial, wraps

class Resource:
    __dispatch__ = 'resource'

    def __init__(self, context, collection=None, record=None):
        self._ctx = context
        self._collection = collection
        self._record = record


class Collection(Resource):
    __resource__ = None

    def __getitem__(self, identifier):
        raise NotImplementedError()
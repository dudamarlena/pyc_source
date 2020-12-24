# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/json.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 1068 bytes
"""
Wrapper for the builtin json module that ensures compliance with the JSON spec.

REST framework should always import this wrapper module in order to maintain
spec-compliant encoding/decoding. Support for non-standard features should be
handled by users at the renderer and parser layer.
"""
from __future__ import absolute_import
import functools, json

def strict_constant(o):
    raise ValueError('Out of range float values are not JSON compliant: ' + repr(o))


@functools.wraps(json.dump)
def dump(*args, **kwargs):
    kwargs.setdefault('allow_nan', False)
    return (json.dump)(*args, **kwargs)


@functools.wraps(json.dumps)
def dumps(*args, **kwargs):
    kwargs.setdefault('allow_nan', False)
    return (json.dumps)(*args, **kwargs)


@functools.wraps(json.load)
def load(*args, **kwargs):
    kwargs.setdefault('parse_constant', strict_constant)
    return (json.load)(*args, **kwargs)


@functools.wraps(json.loads)
def loads(*args, **kwargs):
    kwargs.setdefault('parse_constant', strict_constant)
    return (json.loads)(*args, **kwargs)
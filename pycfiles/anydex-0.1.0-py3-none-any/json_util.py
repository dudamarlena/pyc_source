# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/REST/json_util.py
# Compiled at: 2019-05-22 05:00:30
from __future__ import absolute_import
import json
from collections import Iterable
from six import string_types
__all__ = [
 'dumps', 'loads']

def _is_undumpable(obj):
    """
    Check if JSON can dump an object.

    :param obj: the object to check for dumpability
    :return: the string safe version of the object if undumpable, '' otherwise
    """
    try:
        json.dumps(obj)
        return ''
    except UnicodeDecodeError:
        return repr(obj)


def _scan_iterable(obj, context=None):
    """
    Scan an object for dumpable members if iterable or the dumpability of itself, given some context.

    This recurses over the obj if it is iterable.
    Otherwise, it performs an _is_undumpable() check.

    If the object appears to be undumpable, it will extend the return value with its name added to the current context.

    :param obj: the (possibly iterable) object to check for dumpability
    :param context: the context to report the dumpability of this object for
    :return: a list of undumpable objects in context, represented as lists
    """
    if context is None:
        context = []
    out = []
    if not isinstance(obj, string_types) and isinstance(obj, Iterable):
        for sub in obj:
            if isinstance(obj, dict):
                undumpable = _is_undumpable(sub)
                if undumpable:
                    out += [context + [obj.__class__.__name__ + '::' + repr(sub)]]
                else:
                    out += _scan_iterable(obj[sub], context=context[:] + [
                     obj.__class__.__name__ + '[' + str(sub) + ']'])
            else:
                out += _scan_iterable(sub, context=context[:] + [obj.__class__.__name__])

    else:
        undumpable = _is_undumpable(obj)
        if undumpable:
            out += [context + [obj.__class__.__name__ + '::' + undumpable]]
    return out


def dump(obj, fp, ensure_ascii=True):
    """
    Attempt to json.dump() an object to a 'file'. This function provides additional info if the object can't
    be serialized.

    :param obj: the object to serialize.
    :param fp: the file-like object to write to.
    :param ensure_ascii: allow binary strings to be sent
    """
    try:
        json.dump(obj, fp, ensure_ascii=ensure_ascii)
    except UnicodeDecodeError as e:
        undumpables = _scan_iterable(obj)
        traces = ('\n\t').join([ ('->').join(u) for u in undumpables ])
        error = UnicodeDecodeError(e.encoding, str(obj), e.start, e.end, 'could not dump:\n\t%s' % traces)
        error.message = str(error)
        raise error


def dumps(obj, ensure_ascii=True):
    """
    Attempt to json.dumps() an object. This function provides additional info if the object can't be serialized.

    :param obj: the object to serialize.
    :param ensure_ascii: allow binary strings to be sent
    :return: the JSON str representation of the object.
    """
    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii)
    except UnicodeDecodeError as e:
        undumpables = _scan_iterable(obj)
        traces = ('\n\t').join([ ('->').join(u) for u in undumpables ])
        error = UnicodeDecodeError(e.encoding, str(obj), e.start, e.end, 'could not dump:\n\t%s' % traces)
        error.message = str(error)
        raise error


def loads(s, *args, **kwargs):
    """
    Attempt to json.loads() a string. This function wraps json.loads, to provide dumps and loads from the same file.

    :param s: the JSON formatted string to load objects from.
    :return: the Python object(s) extracted from the JSON input.
    """
    return json.loads(s, *args, **kwargs)


def load(fp, *args, **kwargs):
    """
    Attempt to json.load() from a 'file'. This function wraps json.load, to provide dump and load from the same file.

    :param s: the JSON formatted file-like object to load objects from.
    :return: the Python object(s) extracted from the JSON input.
    """
    return json.load(fp, *args, **kwargs)
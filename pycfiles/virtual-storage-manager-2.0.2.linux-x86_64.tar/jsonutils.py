# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/jsonutils.py
# Compiled at: 2016-06-13 14:11:03
"""
JSON related utilities.

This module provides a few things:

    1) A handy function for getting an object down to something that can be
    JSON serialized.  See to_primitive().

    2) Wrappers around loads() and dumps().  The dumps() wrapper will
    automatically use to_primitive() for you if needed.

    3) This sets up anyjson to use the loads() and dumps() wrappers if anyjson
    is available.
"""
import datetime, functools, inspect, itertools, json, xmlrpclib
from vsm.openstack.common import timeutils

def to_primitive(value, convert_instances=False, convert_datetime=True, level=0, max_depth=3):
    """Convert a complex object into primitives.

    Handy for JSON serialization. We can optionally handle instances,
    but since this is a recursive function, we could have cyclical
    data structures.

    To handle cyclical data structures we could track the actual objects
    visited in a set, but not all objects are hashable. Instead we just
    track the depth of the object inspections and don't go too deep.

    Therefore, convert_instances=True is lossy ... be aware.

    """
    nasty = [
     inspect.ismodule, inspect.isclass, inspect.ismethod,
     inspect.isfunction, inspect.isgeneratorfunction,
     inspect.isgenerator, inspect.istraceback, inspect.isframe,
     inspect.iscode, inspect.isbuiltin, inspect.isroutine,
     inspect.isabstract]
    for test in nasty:
        if test(value):
            return unicode(value)

    if type(value) == itertools.count:
        return unicode(value)
    else:
        if getattr(value, '__module__', None) == 'mox':
            return 'mock'
        if level > max_depth:
            return '?'
        try:
            recursive = functools.partial(to_primitive, convert_instances=convert_instances, convert_datetime=convert_datetime, level=level, max_depth=max_depth)
            if isinstance(value, xmlrpclib.DateTime):
                value = datetime.datetime(*tuple(value.timetuple())[:6])
            if isinstance(value, (list, tuple)):
                return [ recursive(v) for v in value ]
            if isinstance(value, dict):
                return dict((k, recursive(v)) for k, v in value.iteritems())
            if convert_datetime and isinstance(value, datetime.datetime):
                return timeutils.strtime(value)
            if hasattr(value, 'iteritems'):
                return recursive(dict(value.iteritems()), level=level + 1)
            if hasattr(value, '__iter__'):
                return recursive(list(value))
            if convert_instances and hasattr(value, '__dict__'):
                return recursive(value.__dict__, level=level + 1)
            return value
        except TypeError:
            return unicode(value)

        return


def dumps(value, default=to_primitive, **kwargs):
    return json.dumps(value, default=default, **kwargs)


def loads(s):
    return json.loads(s)


def load(s):
    return json.load(s)


try:
    import anyjson
except ImportError:
    pass
else:
    anyjson._modules.append((__name__, 'dumps', TypeError,
     'loads', ValueError, 'load'))
    anyjson.force_implementation(__name__)
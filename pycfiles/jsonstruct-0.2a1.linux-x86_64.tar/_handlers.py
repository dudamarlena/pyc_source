# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jsonstruct/_handlers.py
# Compiled at: 2013-08-09 10:47:32
import sys, datetime, collections, jsonstruct

class DatetimeHandler(jsonstruct.handlers.BaseHandler):
    """
    Datetime objects use __reduce__, and they generate binary strings encoding
    the payload. This handler encodes that payload to reconstruct the
    object.
    """
    _handles = (
     datetime.datetime, datetime.date, datetime.time)

    def flatten(self, obj, data):
        pickler = self._base
        if not pickler.unpicklable:
            return unicode(obj)
        cls, args = obj.__reduce__()
        args = [args[0].encode('base64')] + map(pickler.flatten, args[1:])
        data['__reduce__'] = (pickler.flatten(cls), args)
        return data

    def restore(self, obj):
        cls, args = obj['__reduce__']
        value = args[0].decode('base64')
        unpickler = self._base
        cls = unpickler.restore(cls)
        params = map(unpickler.restore, args[1:])
        params = (value,) + tuple(params)
        return cls.__new__(cls, *params)


class SimpleReduceHandler(jsonstruct.handlers.BaseHandler):
    """
    Follow the __reduce__ protocol to pickle an object. As long as the factory
    and its arguments are pickleable, this should pickle any object that
    implements the reduce protocol.
    """
    _handles = [
     datetime.timedelta]
    if sys.version_info >= (2, 7):
        _handles.append(collections.OrderedDict)

    def flatten(self, obj, data):
        pickler = self._base
        if not pickler.unpicklable:
            return unicode(obj)
        data['__reduce__'] = map(pickler.flatten, obj.__reduce__())
        return data

    def restore(self, obj):
        unpickler = self._base
        factory, args = map(unpickler.restore, obj['__reduce__'])
        return factory(*args)
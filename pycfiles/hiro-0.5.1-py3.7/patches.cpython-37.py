# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/hiro/patches.py
# Compiled at: 2019-10-04 00:47:03
# Size of source mod 2**32: 1425 bytes
"""
patched builtin time classes for use by :class:`hiro.Timeline`
"""
import abc
from datetime import date as realdate
from datetime import datetime as realdatetime
import time, six

class DatetimeMeta(abc.ABCMeta):
    __doc__ = '\n    meta class to allow interaction between :class:`datetime.datetime`\n    objects create inside the :class:`hiro.Timeline` with those created\n    outside it.\n    '

    def __instancecheck__(cls, instance):
        return isinstance(instance, realdatetime)


class DateMeta(type):
    __doc__ = '\n    meta class to allow interaction between :class:`datetime.date`\n    objects create inside the :class:`hiro.Timeline` with those created\n    outside it.\n    '

    def __instancecheck__(cls, instance):
        return isinstance(instance, realdate)


@six.add_metaclass(DatetimeMeta)
class Datetime(realdatetime):
    __doc__ = '\n    used to patch :class:`datetime.datetime` to follow the rules of the\n    parent :class:`hiro.Timeline`\n    '

    @classmethod
    def now(cls, tz=None):
        return cls.fromtimestamp(time.time(), tz)

    @classmethod
    def utcnow(cls):
        return cls.utcfromtimestamp(time.time())


@six.add_metaclass(DateMeta)
class Date(realdate):
    __doc__ = '\n    used to patch :class:`datetime.date` to follow the rules of the\n    parent :class:`hiro.Timeline`\n    '
    __metaclass__ = DateMeta

    @classmethod
    def today(cls):
        return cls.fromtimestamp(time.time())
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flotils\convenience.py
# Compiled at: 2019-04-14 10:12:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2018-19, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2018-01-27'
import abc

def format_vars(instance):
    attrs = vars(instance)
    return (b', ').join((b'{}={}').format(key, value) for key, value in attrs.items())


class FromToDictBase(object):
    """ Class allowing automatic loading to and from dicts of attributes """
    __metaclass__ = abc.ABCMeta

    @classmethod
    def from_dict(cls, d):
        new = cls()
        if not d:
            return new
        attrs = vars(new)
        for key in d:
            if key in attrs:
                setattr(new, key, d[key])

        return new

    def to_dict(self):
        attrs = vars(self)
        res = {}
        for key, value in attrs.items():
            if isinstance(value, FromToDictBase):
                res[key] = value.to_dict()
            else:
                res[key] = value

        return res

    def clone(self):
        return self.from_dict(self.to_dict())


class PrintableBase(object):
    """ Class with auto readable values """
    __metaclass__ = abc.ABCMeta

    def __str__(self):
        return (b'<{}>({})').format(self.__class__.__name__, format_vars(self))

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()
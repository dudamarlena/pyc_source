# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\pkg\nameddict.py
# Compiled at: 2017-04-06 15:23:44
# Size of source mod 2**32: 4517 bytes
__doc__ = '\nSimilar to ``collections.namedtuple``, ``nameddict`` is a data container class.\nProvides methods to iterate on attributes and values.\n\n**中文文档**\n\n和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法\n对属性, 值进行for循环, 以及和list, dict之间的IO交互。\n'
import json, copy
from collections import OrderedDict
from functools import total_ordering

@total_ordering
class Base(object):
    """Base"""
    __attrs__ = None
    __excludes__ = []
    __reserved__ = set(['keys', 'values', 'items'])

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __setattr__(self, attr, value):
        if attr in self.__reserved__:
            raise ValueError('%r is a reserved attribute name!' % attr)
        object.__setattr__(self, attr, value)

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append('%s=%r' % (attr, value))

        return '%s(%s)' % (self.__class__.__name__, ', '.join(kwargs))

    def __getitem__(self, key):
        """Access attribute.
        """
        return object.__getattribute__(self, key)

    @classmethod
    def _make(cls, d):
        """Make an instance.
        """
        return cls(**d)

    def items(self):
        """items按照属性的既定顺序返回attr, value对。当 ``__attrs__`` 未指明时,
        则按照字母顺序返回。若 ``__attrs__`` 已定义时, 按照其中的顺序返回。

        当有 ``@property`` 装饰器所装饰的属性时, 若没有在 ``__attrs__`` 中定义,
        则items中不会包含它。
        """
        items = list()
        if self.__attrs__ is None:
            for key, value in self.__dict__.items():
                if key not in self.__excludes__:
                    items.append((key, value))
                    continue

            items = list(sorted(items, key=lambda x: x[0]))
            return items
        try:
            for attr in self.__attrs__:
                if attr not in self.__excludes__:
                    try:
                        items.append((attr, copy.deepcopy(getattr(self, attr))))
                    except AttributeError:
                        items.append((
                         attr, copy.deepcopy(self.__dict__.get(attr))))

                    continue

            return items
        except:
            raise AttributeError()

    def keys(self):
        """Iterate attributes name.
        """
        return [key for key, value in self.items()]

    def values(self):
        """Iterate attributes value.
        """
        return [value for key, value in self.items()]

    def __iter__(self):
        """Iterate attributes.
        """
        if self.__attrs__ is None:
            return iter(self.keys())
        try:
            return iter(self.__attrs__)
        except:
            raise AttributeError()

    def to_list(self):
        """Export data to list. Will create a new copy for mutable attribute.
        """
        return self.keys()

    def to_dict(self):
        """Export data to dict. Will create a new copy for mutable attribute.
        """
        return dict(self.items())

    def to_OrderedDict(self):
        """Export data to OrderedDict. Will create a new copy for mutable 
        attribute.
        """
        return OrderedDict(self.items())

    def to_json(self):
        """Export data to json. If it is json serilizable.
        """
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        """Equal to.
        """
        return self.items() == other.items()

    def __lt__(self, other):
        """Less than.
        """
        for (_, value1), (_, value2) in zip(self.items(), other.items()):
            if value1 >= value2:
                return False

        return True
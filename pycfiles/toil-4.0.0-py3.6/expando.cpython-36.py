# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/expando.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 2977 bytes
from __future__ import absolute_import

class Expando(dict):
    __doc__ = '\n    Pass inital attributes to the constructor:\n\n    >>> o = Expando(foo=42)\n    >>> o.foo\n    42\n\n    Dynamically create new attributes:\n\n    >>> o.bar = \'hi\'\n    >>> o.bar\n    \'hi\'\n\n    Expando is a dictionary:\n\n    >>> isinstance(o,dict)\n    True\n    >>> o[\'foo\']\n    42\n\n    Works great with JSON:\n\n    >>> import json\n    >>> s=\'{"foo":42}\'\n    >>> o = json.loads(s,object_hook=Expando)\n    >>> o.foo\n    42\n    >>> o.bar = \'hi\'\n    >>> o.bar\n    \'hi\'\n\n    And since Expando is a dict, it serializes back to JSON just fine:\n\n    >>> json.dumps(o, sort_keys=True)\n    \'{"bar": "hi", "foo": 42}\'\n\n    Attributes can be deleted, too:\n\n    >>> o = Expando(foo=42)\n    >>> o.foo\n    42\n    >>> del o.foo\n    >>> o.foo\n    Traceback (most recent call last):\n    ...\n    AttributeError: \'Expando\' object has no attribute \'foo\'\n    >>> o[\'foo\']\n    Traceback (most recent call last):\n    ...\n    KeyError: \'foo\'\n\n    >>> del o.foo\n    Traceback (most recent call last):\n    ...\n    AttributeError: foo\n\n    And copied:\n\n    >>> o = Expando(foo=42)\n    >>> p = o.copy()\n    >>> isinstance(p,Expando)\n    True\n    >>> o == p\n    True\n    >>> o is p\n    False\n\n    Same with MagicExpando ...\n\n    >>> o = MagicExpando()\n    >>> o.foo.bar = 42\n    >>> p = o.copy()\n    >>> isinstance(p,MagicExpando)\n    True\n    >>> o == p\n    True\n    >>> o is p\n    False\n\n    ... but the copy is shallow:\n\n    >>> o.foo is p.foo\n    True\n    '

    def __init__(self, *args, **kwargs):
        (super(Expando, self).__init__)(*args, **kwargs)
        self.__slots__ = None
        self.__dict__ = self

    def copy(self):
        return type(self)(self)


class MagicExpando(Expando):
    __doc__ = "\n    Use MagicExpando for chained attribute access. The first time a missing attribute is\n    accessed, it will be set to a new child MagicExpando.\n\n    >>> o=MagicExpando()\n    >>> o.foo = 42\n    >>> o\n    {'foo': 42}\n    >>> o.bar.hello = 'hi'\n    >>> o.bar\n    {'hello': 'hi'}\n    "

    def __getattribute__(self, name):
        try:
            return super(Expando, self).__getattribute__(name)
        except AttributeError:
            child = self.__class__()
            self[name] = child
            return child
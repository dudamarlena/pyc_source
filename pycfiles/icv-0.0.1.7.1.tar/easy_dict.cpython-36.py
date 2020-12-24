# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/easy_dict.py
# Compiled at: 2019-07-24 07:29:05
# Size of source mod 2**32: 3251 bytes


class EasyDict(dict):
    __doc__ = "\n    Get attributes\n    >>> d = EasyDict({'foo':3})\n    >>> d['foo']\n    3\n    >>> d.foo\n    3\n    >>> d.bar\n    Traceback (most recent call last):\n    ...\n    AttributeError: 'EasyDict' object has no attribute 'bar'\n    Works recursively\n    >>> d = EasyDict({'foo':3, 'bar':{'x':1, 'y':2}})\n    >>> isinstance(d.bar, dict)\n    True\n    >>> d.bar.x\n    1\n    Bullet-proof\n    >>> EasyDict({})\n    {}\n    >>> EasyDict(d={})\n    {}\n    >>> EasyDict(None)\n    {}\n    >>> d = {'a': 1}\n    >>> EasyDict(**d)\n    {'a': 1}\n    Set attributes\n    >>> d = EasyDict()\n    >>> d.foo = 3\n    >>> d.foo\n    3\n    >>> d.bar = {'prop': 'value'}\n    >>> d.bar.prop\n    'value'\n    >>> d\n    {'foo': 3, 'bar': {'prop': 'value'}}\n    >>> d.bar.prop = 'newer'\n    >>> d.bar.prop\n    'newer'\n    Values extraction\n    >>> d = EasyDict({'foo':0, 'bar':[{'x':1, 'y':2}, {'x':3, 'y':4}]})\n    >>> isinstance(d.bar, list)\n    True\n    >>> from operator import attrgetter\n    >>> map(attrgetter('x'), d.bar)\n    [1, 3]\n    >>> map(attrgetter('y'), d.bar)\n    [2, 4]\n    >>> d = EasyDict()\n    >>> d.keys()\n    []\n    >>> d = EasyDict(foo=3, bar=dict(x=1, y=2))\n    >>> d.foo\n    3\n    >>> d.bar.x\n    1\n    Still like a dict though\n    >>> o = EasyDict({'clean':True})\n    >>> o.items()\n    [('clean', True)]\n    And like a class\n    >>> class Flower(EasyDict):\n    ...     power = 1\n    ...\n    >>> f = Flower()\n    >>> f.power\n    1\n    >>> f = Flower({'height': 12})\n    >>> f.height\n    12\n    >>> f['power']\n    1\n    >>> sorted(f.keys())\n    ['height', 'power']\n    update and pop items\n    >>> d = EasyDict(a=1, b='2')\n    >>> e = EasyDict(c=3.0, a=9.0)\n    >>> d.update(e)\n    >>> d.c\n    3.0\n    >>> d['c']\n    3.0\n    >>> d.get('c')\n    3.0\n    >>> d.update(a=4, b=4)\n    >>> d.b\n    4\n    >>> d.pop('a')\n    4\n    >>> d.a\n    Traceback (most recent call last):\n    ...\n    AttributeError: 'EasyDict' object has no attribute 'a'\n    "

    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        if kwargs:
            (d.update)(**kwargs)
        for k, v in d.items():
            setattr(self, k, v)

        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and k not in ('update',
                                                                           'pop'):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x) if isinstance(x, dict) else x for x in value]
        else:
            if isinstance(value, dict):
                if not isinstance(value, self.__class__):
                    value = self.__class__(value)
        super(EasyDict, self).__setattr__(name, value)
        super(EasyDict, self).__setitem__(name, value)

    __setitem__ = __setattr__

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        delattr(self, k)
        return super(EasyDict, self).pop(k, d)

    def dict(self):
        return {k:self[k] for k in self}


if __name__ == '__main__':
    import doctest
    doctest.testmod()
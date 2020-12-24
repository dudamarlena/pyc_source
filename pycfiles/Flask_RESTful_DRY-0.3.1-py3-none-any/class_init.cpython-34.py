# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/class_init.py
# Compiled at: 2015-04-11 15:29:54
# Size of source mod 2**32: 10893 bytes
"""This defines a metaclass that sets up the initial empty class namespace as
derived from the base classes, so that base class variables may be referenced
by the class body that populates the class.

Use :class:`.declarative` as the metaclass for your class to make this work.

Use :class:`.modifier` values in derived classes to modify the inherited values,
rather than replace them.

Use :class:`.attrs` as a bucket of attributes in the base class to allow
individual attribute overrides in derived classes without changing the attrs
in the base class.
"""
import sys
from copy import deepcopy
__all__ = ('declarative', 'attrs', 'modifier', 'extend', 'remove', 'lookup')
debug = False

def set_debug(d):
    global debug
    debug = d


class declarative(type):
    __doc__ = 'Metaclass to provide the inherited attributes to the class body.\n\n    The class body is the code indented under the class declaration.\n\n        >>> class top(metaclass=declarative):\n        ...     x = 1\n        ...     y = attrs(a=5, b=6, c=(1,2,3))\n        >>> class bottom(top):\n        ...     x = x + 1\n        ...     y.b = 22\n        ...     y.c = extend(4,5,6)\n        >>> bottom.x\n        2\n        >>> top.x\n        1\n        >>> bottom.y\n        attrs(a=5, b=22, c=(1, 2, 3, 4, 5, 6))\n        >>> top.y\n        attrs(a=5, b=6, c=(1, 2, 3))\n    '

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return inheriting_dict(bases)

    def __new__(cls, name, bases, namespace, **kwds):
        return super().__new__(cls, name, bases, dict(namespace))


class inheriting_dict(dict):
    __doc__ = "Used as a temporary namespace for class initialization.\n\n    Copies values from the base classes as they are referenced in the class\n    body.\n\n    Used by :class:`.declarative`.\n\n        >>> class a:\n        ...     i = {'x': 1}\n        ...     t = (1,2,3)\n        >>> d = inheriting_dict([a])\n        >>> d.get('i')\n        {'x': 1}\n        >>> d['i']\n        {'x': 1}\n        >>> d['i']['y'] = 12\n        >>> sorted(d['i'].items())\n        [('x', 1), ('y', 12)]\n        >>> a.i\n        {'x': 1}\n        >>> d['t'] = extend(4,5,6)\n        >>> d['t']\n        (1, 2, 3, 4, 5, 6)\n        >>> a.t\n        (1, 2, 3)\n    "

    def __init__(self, bases):
        if debug:
            print('inherited_dict.__init__', bases, file=sys.stderr)
        if not bases:
            self._base = None
        else:
            if len(bases) == 1:
                self._base = bases[0]
            else:
                self._base = type('bogus', bases, {})

    def __getitem__(self, key):
        if debug:
            print('inherited_dict.__getitem__', key, file=sys.stderr)
        try:
            return super().__getitem__(key)
        except KeyError:
            if debug:
                print('inherited_dict.__getitem__ got KeyError', file=sys.stderr)
            if self._base is None:
                raise
            try:
                old_value = getattr(self._base, key)
            except AttributeError:
                if debug:
                    print('inherited_dict.__getitem__ got AttributeError', file=sys.stderr)
                raise KeyError(key)

            new_value = deepcopy(old_value)
            super().__setitem__(key, new_value)
            return new_value

    def get(self, key, default=None):
        if debug:
            print('inherited_dict.get', key, file=sys.stderr)
        try:
            return super().__getitem__(key)
        except KeyError:
            if debug:
                print('inherited_dict.get got KeyError', file=sys.stderr)
            if self._base is None:
                return default
            else:
                try:
                    old_value = getattr(self._base, key)
                except AttributeError:
                    if debug:
                        print('inherited_dict.__getitem__ got AttributeError', file=sys.stderr)
                    return default

                new_value = deepcopy(old_value)
                super().__setitem__(key, new_value)
                return new_value

    def __setitem__(self, key, value):
        """Need this to be able to assign a :class:`.modifier` to values.
        """
        if debug:
            print('inherited_dict.__setitem__', key, value, file=sys.stderr)
        if isinstance(value, modifier):
            if debug:
                print('inherited_dict.__setitem__', key, 'modifying', file=sys.stderr)
            super().__setitem__(key, value.update_value(self.get(key), self))
        else:
            super().__setitem__(key, value)
        if debug:
            print('inherited_dict.__setitem__', key, 'done', file=sys.stderr)


class attrs:
    __doc__ = "Tracks which attributes have been set in _names.\n\n    _names is a set.\n\n        >>> a = attrs(x=1,y=2,z=3)\n        >>> sorted(a._names)\n        ['x', 'y', 'z']\n        >>> a.x\n        1\n        >>> a.w = 44\n        >>> a.w\n        44\n        >>> sorted(a._names)\n        ['w', 'x', 'y', 'z']\n\n    Provides a :method:`.copy` method to make a deep copy of the attrs\n    object (calling copy on all attrs values).\n\n        >>> bottom = attrs(z='bottom')\n        >>> middle = attrs(b=bottom, y='middle')\n        >>> top = attrs(m=middle, x='top')\n        >>> top.m.b.z\n        'bottom'\n        >>> c = deepcopy(top)\n        >>> c.m.b.z = 'c'\n        >>> c.m.b.z\n        'c'\n        >>> top.m.b.z\n        'bottom'\n\n    Also provides a :method:`.copy_into` to copy its attributes into another\n    object.  This does not copy any attribute names starting with '_'.\n\n        >>> class other: pass\n        >>> b = other()\n        >>> b.x = 'b'\n        >>> b._hidden = 'b'\n        >>> top._hidden = 'top'\n        >>> top.copy_into(b)\n        >>> b.m.b.z\n        'bottom'\n        >>> b.x\n        'top'\n        >>> b._hidden\n        'b'\n        >>> b.m.b.z = 'b'\n        >>> b.m.b.z\n        'b'\n        >>> top.m.b.z\n        'bottom'\n    "

    def __init__(self, **attrs):
        for key, value in attrs.items():
            super().__setattr__(key, deepcopy(value))

        self._names = set(attrs.keys())

    def __repr__(self):
        return 'attrs({})'.format(', '.join('{}={!r}'.format(name, getattr(self, name)) for name in sorted(self._names)))

    def __setattr__(self, key, value):
        if key[0] != '_':
            self._names.add(key)
        if isinstance(value, modifier):
            current_value = getattr(self, key, None)
            if current_value is None:
                super().__setattr__(key, deepcopy(value))
            else:
                if isinstance(current_value, modifier):
                    super().__setattr__(key, value.update_modifier(current_value))
                else:
                    super().__setattr__(key, value.update_value(current_value, self))
        else:
            super().__setattr__(key, deepcopy(value))

    def copy_into(self, obj):
        for name in self._names:
            value = deepcopy(getattr(self, name))
            if isinstance(value, modifier):
                setattr(obj, name, value.update_value(getattr(obj, name, None), obj))
            else:
                setattr(obj, name, value)


class modifier:
    __doc__ = "Base class for all modifiers.\n\n    Subclass must define update_modifier(orig_modifier) and update_value(obj,\n    parent) methods.\n\n    The update_modifier method is called to merge self into an existing\n    modifier that is already stored on the target object.  It should check the\n    type of it's argument (it could be anything).\n\n    The update_value method is called to modify a non-modifier value that is\n    already stored on the object.\n    "


class extend(modifier):
    __doc__ = 'Used by :class:`.attrs` to extend a value, rather than replacing it.\n\n    Also changes the constructor to take multiple arguments, rather than a\n    single argument.\n\n        >>> extend(1,2,3)\n        extend(1, 2, 3)\n        >>> class other: pass\n        >>> b = other()\n        >>> b.t = (1,2,3)\n        >>> a = attrs(t=extend(4,5,6))\n        >>> a.copy_into(b)\n        >>> b.t\n        (1, 2, 3, 4, 5, 6)\n    '

    def __init__(self, *values):
        self.values = values

    def __repr__(self):
        return 'extend({})'.format(', '.join(repr(x) for x in self.values))

    def update_modifier(self, orig):
        if not isinstance(orig, extend):
            raise ValueError("Can't combine an 'extend' object with a '{}' object".format(orig.__class__.__name__))
        return extend(*(self.values + orig.values))

    def update_value(self, obj, parent):
        if not isinstance(obj, tuple):
            raise ValueError("Can only extend a tuple, not a '{}' object".format(obj.__class__.__name__))
        return obj + self.values


class remove(modifier):
    __doc__ = 'Used by :class:`.attrs` to remove items from a tuple.\n\n        >>> remove(1,2,3)\n        remove(1, 2, 3)\n        >>> class other: pass\n        >>> b = other()\n        >>> b.t = (1,2,3)\n        >>> a = attrs(t=remove(1,3))\n        >>> a.copy_into(b)\n        >>> b.t\n        (2,)\n    '

    def __init__(self, *values):
        self.values = values

    def __repr__(self):
        return 'remove({})'.format(', '.join(repr(x) for x in self.values))

    def update_modifier(self, orig):
        if not isinstance(orig, remove):
            raise ValueError("Can't combine a 'remove' object with a '{}' object".format(orig.__class__.__name__))
        return remove(*(self.values + orig.values))

    def update_value(self, obj, parent):
        if isinstance(obj, str) or not hasattr(obj, '__iter__'):
            raise ValueError("Can only remove from a sequence, not a '{}' object".format(obj.__class__.__name__))
        return tuple(x for x in obj if x not in self.values)


class lookup(modifier):
    __doc__ = "Looks up a dotted reference in the object that it's copied into.\n\n        >>> lookup('a.b')\n        lookup('a.b')\n        >>> class other: pass\n        >>> b = other()\n        >>> b.t = (1,2,3)\n        >>> b.a = other()\n        >>> b.a.b = 'hi mom'\n        >>> a = attrs(t=lookup('a.b'))\n        >>> a.copy_into(b)\n        >>> b.t\n        'hi mom'\n    "

    def __init__(self, reference):
        self.references = tuple(reference.split('.'))

    def __repr__(self):
        return "lookup('{}')".format('.'.join(self.references))

    def update_modifier(self, orig):
        """Overrides any other value or modifier.
        """
        return self

    def update_value(self, obj, parent):
        ans = parent
        for attr in self.references:
            ans = getattr(ans, attr)

        return ans
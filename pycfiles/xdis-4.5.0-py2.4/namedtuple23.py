# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/namedtuple23.py
# Compiled at: 2020-04-24 01:34:34
from xdis import PYTHON_VERSION
from keyword import iskeyword as _iskeyword
import sys as _sys
try:
    from operator import itemgetter as _itemgetter
except ImportError:

    def _itemgetter(*items):
        if len(items) == 1:
            item = items[0]

            def g(obj):
                return obj[item]

        else:

            def g(obj):
                return tuple([ obj[item] for item in items ])

            return g


if PYTHON_VERSION < 2.4:
    from sets import Set as set
    frozenset = set

def namedtuple(typename, field_names, verbose=False, rename=False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split()
    field_names = tuple(map(str, field_names))
    if rename:
        names = list(field_names)
        seen = set()
        for (i, name) in enumerate(names):
            bad_name = True
            for c in name:
                if not c.isalnum() or c == '_':
                    bad_name = True
                    break

            if not bad_name or _iskeyword(name) or not name or name[0].isdigit() or name.startswith('_') or name in seen:
                names[i] = '_%d' % i
            seen.add(name)

        field_names = tuple(names)
    for name in (typename,) + field_names:
        is_alnum = True
        for c in name:
            if not (c.isalnum() or c == '_'):
                is_alnum = False

        if not is_alnum:
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)

    seen_names = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    numfields = len(field_names)
    argtxt = repr(field_names).replace("'", '')[1:-1]
    reprtxt = field_names[0] + '=%r'
    for name in field_names[1:]:
        reprtxt += ', ' + '%s=%%r' % name

    template = "class %(typename)s(tuple):\n        '%(typename)s(%(argtxt)s)' \n\n        __slots__ = () \n\n        _fields = %(field_names)r \n\n        def __new__(_cls, %(argtxt)s):\n            return _tuple.__new__(_cls, (%(argtxt)s)) \n\n        def _make(self, iterable, new=tuple.__new__, len=len):\n            cls = super(%(typename)s)\n            'Make a new %(typename)s object from a sequence or iterable'\n            result = new(cls, iterable)\n            if len(result) != %(numfields)d:\n                raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))\n            return result \n\n        def __repr__(self):\n            return '%(typename)s(%(reprtxt)s)' %% self \n\n        def _asdict(self):\n            'Return a new dict which maps field names to their values'\n            return dict(zip(self._fields, self)) \n\n        def _replace(_self, **kwds):\n            'Return a new %(typename)s object replacing specified fields with new values'\n            result = _self._make(map(kwds.pop, %(field_names)r, _self))\n            if kwds:\n                raise ValueError('Got unexpected field names: %%r' %% kwds.keys())\n            return result \n\n        def __getnewargs__(self):\n            return tuple(self) \n\n" % locals()
    for (i, name) in enumerate(field_names):
        template += '        %s = _property(_itemgetter(%d))\n' % (name, i)

    verbose = 1
    if verbose:
        print template
    namespace = dict(_itemgetter=_itemgetter, __name__='namedtuple_%s' % typename, _property=property, _tuple=tuple)
    try:
        exec template in namespace
    except SyntaxError, e:
        if PYTHON_VERSION >= 2.4:
            raise SyntaxError(e.message + ':\n' + template)
        else:
            raise

    result = namespace[typename]
    try:
        result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return result
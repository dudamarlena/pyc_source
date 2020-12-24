# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/utils/record_type.py
# Compiled at: 2013-01-15 04:29:08
__all__ = ['recordtype']
__author__ = 'http://code.activestate.com/recipes/576555/'
import sys
from textwrap import dedent
from keyword import iskeyword

def recordtype(typename, field_names, verbose=False, **default_kwds):
    """
        Returns a new class with named fields.

        field_defaults: A mapping from (a subset of) field names to default
            values.
        default: If provided, the default value for all fields without an
            explicit default in `field_defaults`.

        >>> Point = recordtype('Point', 'x y', default=0)
        >>> Point.__doc__           # docstring for the new class
        'Point(x, y)'
        >>> Point()                 # instantiate with defaults
        Point(x=0, y=0)
        >>> p = Point(11, y=22)     # instantiate with positional args or keywords
        >>> p[0] + p.y              # accessible by name and index
        33
        >>> p.x = 100; p[1] =200    # modifiable by name and index
        >>> p
        Point(x=100, y=200)
        >>> x, y = p               # unpack
        >>> x, y
        (100, 200)
        >>> d = p.todict()         # convert to a dictionary
        >>> d['x']
        100
        >>> Point(**d) == p        # convert from a dictionary
        True
    """
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split()
    field_names = tuple(map(str, field_names))
    if not field_names:
        raise ValueError('Records must have at least one field')
    for name in (typename,) + field_names:
        if not min(c.isalnum() or c == '_' for c in name):
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)

    seen_names = set()
    for name in field_names:
        if name.startswith('_'):
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    field_defaults = default_kwds.pop('field_defaults', {})
    if 'default' in default_kwds:
        default = default_kwds.pop('default')
        init_defaults = tuple(field_defaults.get(f, default) for f in field_names)
    else:
        if not field_defaults:
            init_defaults = None
        else:
            default_fields = field_names[-len(field_defaults):]
            if set(default_fields) != set(field_defaults):
                raise ValueError('Missing default parameter values')
            init_defaults = tuple(field_defaults[f] for f in default_fields)
        if default_kwds:
            raise ValueError('Invalid keyword arguments: %s' % default_kwds)
        numfields = len(field_names)
        argtxt = (', ').join(field_names)
        reprtxt = (', ').join('%s=%%r' % f for f in field_names)
        dicttxt = (', ').join('%r: self.%s' % (f, f) for f in field_names)
        tupletxt = repr(tuple('self.%s' % f for f in field_names)).replace("'", '')
        inittxt = ('; ').join('self.%s=%s' % (f, f) for f in field_names)
        itertxt = ('; ').join('yield self.%s' % f for f in field_names)
        eqtxt = (' and ').join('self.%s==other.%s' % (f, f) for f in field_names)
        template = dedent("\n        class %(typename)s(object):\n            '%(typename)s(%(argtxt)s)'\n\n            __slots__  = %(field_names)r\n\n            def __init__(self, %(argtxt)s):\n                %(inittxt)s\n\n            def __len__(self):\n                return %(numfields)d\n\n            def __iter__(self):\n                %(itertxt)s\n\n            def __getitem__(self, index):\n                return getattr(self, self.__slots__[index])\n\n            def __setitem__(self, index, value):\n                return setattr(self, self.__slots__[index], value)\n\n            def todict(self):\n                'Return a new dict which maps field names to their values'\n                return {%(dicttxt)s}\n\n            def __repr__(self):\n                return '%(typename)s(%(reprtxt)s)' %% %(tupletxt)s\n\n            def __eq__(self, other):\n                return isinstance(other, self.__class__) and %(eqtxt)s\n\n            def __ne__(self, other):\n                return not self==other\n\n            def __getstate__(self):\n                return %(tupletxt)s\n\n            def __setstate__(self, state):\n                %(tupletxt)s = state\n    ") % locals()
        namespace = {}
        try:
            exec template in namespace
            if verbose:
                print template
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + template)

    cls = namespace[typename]
    cls.__init__.im_func.func_defaults = init_defaults
    if hasattr(sys, '_getframe') and sys.platform != 'cli':
        cls.__module__ = sys._getframe(1).f_globals['__name__']
    return cls


if __name__ == '__main__':
    import doctest
    TestResults = recordtype('TestResults', 'failed, attempted')
    print TestResults(*doctest.testmod())
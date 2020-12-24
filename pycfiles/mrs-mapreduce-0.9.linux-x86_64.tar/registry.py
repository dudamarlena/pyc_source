# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amcnabb/python/mrs/registry.py
# Compiled at: 2012-10-25 15:03:27
"""Function Registry

The master and slaves need to agree on what functions are available and what
they are called.  A Registry is established before determining the
master/slave roles.  Then everyone can agree on what the names mean.
"""

def object_hash(obj):
    """Hash an object x based on its code.

    If it's a function, hash its code.  Otherwise, hash all of the functions
    in its attributes (excepting attributes beginning with two underscores).
    Note that if the object has no methods or only built-in methods, the hash
    may be 0.

    Hashing of functions:

    >>> def f(x):
    ...   return x**2
    >>> def g(y):
    ...   return y**2
    >>> object_hash(f) == 0
    False
    >>> object_hash(f) == object_hash(g)
    True
    >>>

    Hashing of classes:

    >>> class A(object):
    ...   def __init__(self, x):
    ...     self.x = x
    ...   def f(self):
    ...     return self.x**2
    ...   def g(self):
    ...     return self.x**3
    >>> class B(object):
    ...   def __init__(self):
    ...     self.x = 3
    ...   def f(self):
    ...     return self.x**2
    ...   def g(self):
    ...     return self.x**3
    >>> class C(object):
    ...   def __init__(self, x):
    ...     self.x = x
    ...   def g(self):
    ...     return self.x**3
    >>>
    >>> object_hash(A) == 0
    False
    >>> object_hash(A) == object_hash(B)
    True
    >>> object_hash(A) == object_hash(C)
    False
    >>>

    Hashing of instances:

    >>> a1 = A(4)
    >>> a2 = A(5)
    >>> b = B()
    >>> object_hash(a1) == 0
    False
    >>> object_hash(a1) == object_hash(a2)
    True
    >>> object_hash(a1) == object_hash(b)
    True
    >>>
    """
    try:
        code = obj.__code__.co_code
    except AttributeError:
        attrlist = [ getattr(obj, name) for name in dir(obj) if not name.startswith('__')
                   ]
        codelist = [ attr.__code__.co_code for attr in attrlist if hasattr(attr, '__code__')
                   ]
        code = (',').join(codelist)

    return str(hash(code))


class Registry(object):
    """Manage a mapping between methods and their names.

    A Registry keeps track of all attributes of an object that can be stored
    in a dict.  Any attributes that cannot be keys, such as lists, are
    ignored.

    >>> class A(object):
    ...   lst = [1, 2, 3]
    ...   def f(self):
    ...     return 1
    ...   def g(self):
    ...     return 2
    >>> a = A()
    >>> r = Registry(a)
    >>> r[a.f]
    'f'
    >>> r[a.g]
    'g'
    >>> getattr(a, r[a.f]) == a.f
    True
    >>>
    """

    def __init__(self, program):
        self.program = program
        self.attrs = {}
        for name in dir(program):
            if not name.startswith('__'):
                attr = getattr(program, name)
                try:
                    self.attrs[attr] = name
                except TypeError:
                    pass

    def __getitem__(self, attr):
        try:
            return self.attrs[attr]
        except KeyError:
            raise KeyError('Value is not an attribute of the user program')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
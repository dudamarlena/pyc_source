# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/lib/typelib.py
# Compiled at: 2008-04-06 04:02:05
"""
================================
 Type Class Library: typelib.py
================================
version 1.0 (2000-03-27)

Homepage: [[http://gotools.sourceforge.net/]] (see sgflib.py)

Copyright (C) 2000 David John Goodger ([[mailto:dgoodger@bigfoot.com]]).
typelib.py comes with ABSOLUTELY NO WARRANTY. This is free software, and you are
welcome to redistribute it and/or modify it under certain conditions; see the
source code for details.

Description
===========
This library implements abstract superclasses to emulate Python's built-in data
types. This is useful when you want a class which acts like a built-in type, but
with added/modified behaviour (methods) and/or data (attributes).

Implemented types are: 'String', 'Tuple', 'List', 'Dictionary', 'Integer',
'Long', 'Float', 'Complex' (along with their abstract superclasses).

All methods, including special overloading methods, are implemented for each
type-emulation class. Instance data is stored internally in the 'data' attribute
(i.e., 'self.data'). The type the class is emulating is stored in the class
attribute 'self.TYPE' (as given by the built-in 'type(class)').  The
'SuperClass.__init__()' method uses two class-specific methods to instantiate
objects: '_reset()' and '_convert()'.

See "sgflib.py" (at module's homepage, see above) for examples of use. The Node
class is of particular interest: a modified 'Dictionary' which is ordered and
allows for offset-indexed retrieval."""

class SuperType:
    """ Superclass of all type classes. Implements methods common to all types.
                Concrete (as opposed to abstract) subclasses must define a class
                attribute 'self.TYPE' ('=type(Class)'), and methods '_reset(self)' and
                '_convert(self, data)'."""
    __module__ = __name__

    def __init__(self, data=None):
        """
                On 'Class()', initialize 'self.data'. Argument:
                - 'data' : optional, default 'None' --
                        - If the type of 'data' is identical to the Class' 'TYPE',
                          'data' will be shared (relevant for mutable types only).
                        - If 'data' is given (and not false), it will be converted by
                          the Class-specific method 'self._convert(data)'. Incompatible
                          data types will raise an exception.
                        - If 'data' is 'None', false, or not given, a Class-specific method
                          'self._reset()' is called to initialize an empty instance."""
        if data:
            if type(data) is self.TYPE:
                self.data = data
            else:
                self.data = self._convert(data)
        else:
            self._reset()

    def __str__(self):
        """ On 'str(self)' and 'print self'. Returns string representation."""
        return str(self.data)

    def __cmp__(self, x):
        """        On 'self>x', 'self==x', 'cmp(self,x)', etc. Catches all
                        comparisons: returns -1, 0, or 1 for less, equal, or greater."""
        return cmp(self.data, x)

    def __rcmp__(self, x):
        """        On 'x>self', 'x==self', 'cmp(x,self)', etc. Catches all
                        comparisons: returns -1, 0, or 1 for less, equal, or greater."""
        return cmp(x, self.data)

    def __hash__(self):
        """ On 'dictionary[self]', 'hash(self)'. Returns a unique and unchanging
                        integer hash-key."""
        return hash(self.data)


class AddMulMixin:
    """ Addition & multiplication for numbers, concatenation & repetition for
                sequences."""
    __module__ = __name__

    def __add__(self, other):
        """ On 'self+other'. Numeric addition, or sequence concatenation."""
        return self.data + other

    def __radd__(self, other):
        """ On 'other+self'. Numeric addition, or sequence concatenation."""
        return other + self.data

    def __mul__(self, other):
        """ On 'self*other'. Numeric multiplication, or sequence repetition."""
        return self.data * other

    def __rmul__(self, other):
        """ On 'other*self'. Numeric multiplication, or sequence repetition."""
        return other * self.data


class MutableMixin:
    """ Assignment to and deletion of collection component."""
    __module__ = __name__

    def __setitem__(self, key, x):
        """ On 'self[key]=x'."""
        self.data[key] = x

    def __delitem__(self, key):
        """ On 'del self[key]'."""
        del self.data[key]


class ModMixin:
    """ Modulo remainder and string formatting."""
    __module__ = __name__

    def __mod__(self, other):
        """ On 'self%other'."""
        return self.data % other

    def __rmod__(self, other):
        """ On 'other%self'."""
        return other % self.data


class Number(SuperType, AddMulMixin, ModMixin):
    """ Superclass for numeric emulation types."""
    __module__ = __name__

    def __sub__(self, other):
        """ On 'self-other'."""
        return self.data - other

    def __rsub__(self, other):
        """ On 'other-self'."""
        return other - self.data

    def __div__(self, other):
        """ On 'self/other'."""
        return self.data / other

    def __rdiv__(self, other):
        """ On 'other/self'."""
        return other / self.data

    def __divmod__(self, other):
        """ On 'divmod(self,other)'."""
        return divmod(self.data, other)

    def __rdivmod__(self, other):
        """ On 'divmod(other,self)'."""
        return divmod(other, self.data)

    def __pow__(self, other, mod=None):
        """ On 'pow(self,other[,mod])', 'self**other'."""
        if mod is None:
            return self.data ** other
        else:
            return pow(self.data, other, mod)
        return

    def __rpow__(self, other):
        """ On 'pow(other,self)', 'other**self'."""
        return other ** self.data

    def __neg__(self):
        """ On '-self'."""
        return -self.data

    def __pos__(self):
        """ On '+self'."""
        return +self.data

    def __abs__(self):
        """ On 'abs(self)'."""
        return abs(self.data)

    def __int__(self):
        """ On 'int(self)'."""
        return int(self.data)

    def __long__(self):
        """ On 'long(self)'."""
        return long(self.data)

    def __float__(self):
        """ On 'float(self)'."""
        return float(self.data)

    def __complex__(self):
        """ On 'complex(self)'."""
        return complex(self.data)

    def __nonzero__(self):
        """ On truth-value (or uses '__len__()' if defined)."""
        return self.data != 0

    def __coerce__(self, other):
        """ On mixed-type expression, 'coerce()'. Returns tuple of '(self, other)'
                        converted to a common type."""
        return coerce(self.data, other)


class Integer(Number):
    """ Emulates a Python integer."""
    __module__ = __name__
    TYPE = type(1)

    def _reset(self):
        """ Initialize an integer."""
        self.data = 0

    def _convert(self, data):
        """ Convert data into an integer."""
        return int(data)

    def __lshift__(self, other):
        """ On 'self<<other'."""
        return self.data << other

    def __rlshift__(self, other):
        """ On 'other<<self'."""
        return other << self.data

    def __rshift__(self, other):
        """ On 'self>>other'."""
        return self.data >> other

    def __rrshift__(self, other):
        """ On 'other>>self'."""
        return other >> self.data

    def __and__(self, other):
        """ On 'self&other'."""
        return self.data & other

    def __rand__(self, other):
        """ On 'other&self'."""
        return other & self.data

    def __or__(self, other):
        """ On 'self|other'."""
        return self.data | other

    def __ror__(self, other):
        """ On 'other|self'."""
        return other | self.data

    def __xor__(self, other):
        """ On 'self^other'."""
        return self.data ^ other

    def __rxor__(self, other):
        """ On 'other%self'."""
        return other % self.data

    def __invert__(self):
        """ On '~self'."""
        return ~self.data

    def __oct__(self):
        """ On 'oct(self)'. Returns octal string representation."""
        return oct(self.data)

    def __hex__(self):
        """ On 'hex(self)'. Returns hexidecimal string representation."""
        return hex(self.data)


class Long(Integer):
    """ Emulates a Python long integer."""
    __module__ = __name__
    TYPE = type(1)

    def _reset(self):
        """ Initialize an integer."""
        self.data = 0

    def _convert(self, data):
        """ Convert data into an integer."""
        return long(data)


class Float(Number):
    """ Emulates a Python floating-point number."""
    __module__ = __name__
    TYPE = type(0.1)

    def _reset(self):
        """ Initialize a float."""
        self.data = 0.0

    def _convert(self, data):
        """ Convert data into a float."""
        return float(data)


class Complex(Number):
    """ Emulates a Python complex number."""
    __module__ = __name__
    TYPE = type(0 + complex(0.0, 0.0))

    def _reset(self):
        """ Initialize an integer."""
        self.data = 0 + complex(0.0, 0.0)

    def _convert(self, data):
        """ Convert data into an integer."""
        return complex(data)

    def __getattr__(self, name):
        """ On 'self.real' & 'self.imag'."""
        if name == 'real':
            return self.data.real
        elif name == 'imag':
            return self.data.imag
        else:
            raise AttributeError(name)

    def conjugate(self):
        """ On 'self.conjugate()'."""
        return self.data.conjugate()


class Container(SuperType):
    """ Superclass for countable, indexable collection types ('Sequence', 'Mapping')."""
    __module__ = __name__

    def __len__(self):
        """ On 'len(self)', truth-value tests. Returns sequence or mapping
                        collection size. Zero means false."""
        return len(self.data)

    def __getitem__(self, key):
        """ On 'self[key]', 'x in self', 'for x in self'. Implements all
                        indexing-related operations. Membership and iteration ('in', 'for')
                        repeatedly index from 0 until 'IndexError'."""
        return self.data[key]


class Sequence(Container, AddMulMixin):
    """ Superclass for classes which emulate sequences ('List', 'Tuple', 'String')."""
    __module__ = __name__

    def __getslice__(self, low, high):
        """ On 'self[low:high]'."""
        return self.data[low:high]


class String(Sequence, ModMixin):
    """ Emulates a Python string."""
    __module__ = __name__
    TYPE = type('')

    def _reset(self):
        """ Initialize an empty string."""
        self.data = ''

    def _convert(self, data):
        """ Convert data into a string."""
        return str(data)


class Tuple(Sequence):
    """ Emulates a Python tuple."""
    __module__ = __name__
    TYPE = type(())

    def _reset(self):
        """ Initialize an empty tuple."""
        self.data = ()

    def _convert(self, data):
        """ Non-tuples cannot be converted. Raise an exception."""
        raise TypeError('Non-tuples cannot be converted to a tuple.')


class MutableSequence(Sequence, MutableMixin):
    """ Superclass for classes which emulate mutable (modifyable in-place)
                sequences ('List')."""
    __module__ = __name__

    def __setslice__(self, low, high, seq):
        """ On 'self[low:high]=seq'."""
        self.data[low:high] = seq

    def __delslice__(self, low, high):
        """ On 'del self[low:high]'."""
        del self.data[low:high]

    def append(self, x):
        """ Inserts object 'x' at the end of 'self.data' in-place."""
        self.data.append(x)

    def count(self, x):
        """ Returns the number of occurrences of 'x' in 'self.data'."""
        return self.data.count(x)

    def extend(self, x):
        """ Concatenates sequence 'x' to the end of 'self' in-place 
                        (like 'self=self+x')."""
        self.data.extend(x)

    def index(self, x):
        """ Returns the offset of the first occurrence of object 'x' in
                        'self.data'; raises an exception if not found."""
        return self.data.index(x)

    def insert(self, i, x):
        """ Inserts object 'x' into 'self.data' at offset 'i' 
                        (like 'self[i:i]=[x]')."""
        self.data.insert(i, x)

    def pop(self, i=-1):
        """ Returns and deletes the last item of 'self.data' (or item
                        'self.data[i]' if 'i' given)."""
        return self.data.pop(i)

    def remove(self, x):
        """ Deletes the first occurrence of object 'x' from 'self.data'; 
                        raise an exception if not found."""
        self.data.remove(x)

    def reverse(self):
        """ Reverses items in 'self.data' in-place."""
        self.data.reverse()

    def sort(self, func=None):
        """
                Sorts 'self.data' in-place. Argument:
                - func : optional, default 'None' --
                        - If 'func' not given, sorting will be in ascending
                          order.
                        - If 'func' given, it will determine the sort order.
                          'func' must be a two-argument comparison function
                          which returns -1, 0, or 1, to mean before, same,
                          or after ordering."""
        if func:
            self.data.sort(func)
        else:
            self.data.sort()


class List(MutableSequence):
    """ Emulates a Python list. When instantiating an object with data
                ('List(data)'), you can force a copy with 'List(list(data))'."""
    __module__ = __name__
    TYPE = type([])

    def _reset(self):
        """ Initialize an empty list."""
        self.data = []

    def _convert(self, data):
        """ Convert data into a list."""
        return list(data)


class Mapping(Container):
    """ Superclass for classes which emulate mappings/hashes ('Dictionary')."""
    __module__ = __name__

    def has_key(self, key):
        """ Returns 1 (true) if 'self.data' has a key 'key', or 0 otherwise."""
        return self.data.has_key(key)

    def keys(self):
        """ Returns a new list holding all keys from 'self.data'."""
        return self.data.keys()

    def values(self):
        """ Returns a new list holding all values from 'self.data'."""
        return self.data.values()

    def items(self):
        """ Returns a new list of tuple pairs '(key, value)', one for each entry
                        in 'self.data'."""
        return self.data.items()

    def clear(self):
        """ Removes all items from 'self.data'."""
        self.data.clear()

    def get(self, key, default=None):
        """ Similar to 'self[key]', but returns 'default' (or 'None') instead of
                        raising an exception when 'key' is not found in 'self.data'."""
        return self.data.get(key, default)

    def copy(self):
        """ Returns a shallow (top-level) copy of 'self.data'."""
        return self.data.copy()

    def update(self, dict):
        """ Merges 'dict' into 'self.data' 
                        (i.e., 'for (k,v) in dict.items(): self.data[k]=v')."""
        self.data.update(dict)


class Dictionary(Mapping, MutableMixin):
    """ Emulates a Python dictionary, a mutable mapping. When instantiating an
                object with data ('Dictionary(data)'), you can force a (shallow) copy
                with 'Dictionary(data.copy())'."""
    __module__ = __name__
    TYPE = type({})

    def _reset(self):
        """ Initialize an empty dictionary."""
        self.data = {}

    def _convert(self, data):
        """ Non-dictionaries cannot be converted. Raise an exception."""
        raise TypeError('Non-dictionaries cannot be converted to a dictionary.')


if __name__ == '__main__':
    print __doc__
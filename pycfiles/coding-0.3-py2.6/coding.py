# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/coding.py
# Compiled at: 2013-06-29 03:57:40
"""
Coding is a base class which provides an answer to the issue of how to
create enums in python.
"""
from __future__ import unicode_literals, print_function
__docformat__ = b'restructuredtext en'

class Coding(object):
    '''
    This class is related to the way that enums are handled in C.  It
    is intended to be subclassed rather than instantiated directly.

    Each subclass comprises an independent type which is suitable for
    type checking as well as a grouping of (name, code, closure)
    triples.  Each instance of a subclass represents a specific (name,
    code, closure) triple.  Within a subclass, items can be looked up
    by name or by code or traversed by name or by code.

    For example::

        import coding

        class PeopleCoding(coding.Coding):

            """
            This is a group of people.  Closure is used here as a
            description but in other subclasses it could be used to
            represent just about anything including function pointers
            or closures.
            """
            bycode = byname = {} # so PeopleCoding will have it's own
                                 # dicts rather than sharing those of
                                 # the base class

        PeopleCoding('Bob', 1, 'This code represents Bob.')
        PeopleCoding('Carol', 2, 'Carol represented here')
        PeopleCoding('Ted', 3, 'Better Ted than Fred')
        PeopleCoding('Alice', 4, 'Doesn't live here anymore')

    You can now lookup codes::

        PeopleCoding.byname['Bob'].code

    Or names::

        PeopleCoding.bycode[3].name

    Closures by code::

        PeopleCoding.bycode[3].closure

    Or by name::

        PeopleCoding.byname['Bob'].closure

    Type conversions work as one might expect and, for convenience,
    the call value of an instance is the closure::

        x = PeopleCoding.bycode[3]
        assert x.name == str(x)
        assert x.code == int(x)
        assert x.closure == x()

    You can list all codes in this class::

        [code for code in PeopleCoding.bycode]

    Or all names::

        [name for name in PeopleCoding.byname]

    You can test for inclusion by name::

        'Herman' in PeopleCoding.byname

    Or by code::

        2 in PeopleCoding.bycode

    Note that each subclass of Coding represents a unique type::

        assert isinstance(PeopleCoding.bycode[3], PeopleCoding)

    .. note:: Also note that codings should be considered immutable.

    .. todo:: Since the class wraps access to data attibutes, there's
        no reason it couldn't rework the dictionaries to support
        mutable instances.  (Just make sure that when removing items
        from a dict, we remove the right items rather than some other
        item with the same key.)

    .. todo:: support for removing instances.

    .. todo:: class should include an aggregator for all instances.
        This will be different from iterating over the dicts when
        field overloading is in effect.
    '''
    byname = {}
    overload_names = False
    bycode = {}
    overload_codes = False

    def __init__(self, name=b'', code=0, closure=None):
        """
        Create a coding instance.
        """
        self._name = name
        self._code = code
        self._closure = closure
        if not self.overload_names and name in self.byname or not self.overload_codes and code in self.bycode:
            raise KeyError
        self.byname[name] = self
        self.bycode[code] = self

    @property
    def name(self):
        """name accessor"""
        return self._name

    @name.setter
    def name(self, value):
        """name setter"""
        raise NotImplementedError

    @property
    def code(self):
        """code accessor"""
        return self._code

    @code.setter
    def code(self, value):
        """code setter"""
        raise NotImplementedError

    @property
    def closure(self):
        """closure accessor"""
        return self._closure

    @closure.setter
    def closure(self, value):
        """closure setter"""
        raise NotImplementedError

    def __index__(self):
        return self.code

    def __hash__(self):
        return self.code

    def __int__(self):
        return self.code

    def __call__(self):
        return self.closure

    def __repr__(self):
        return (b'{0}(name={1}, code={2}, closure={3})').format(self.__class__.__name__, self.name, self.code, self.closure)

    def __str__(self):
        return self.name


class NameMajorCoding(Coding):
    """
    *NameMajorCoding* is a subclass of *Coding* and as such inherits
    all of the functionality of the Coding class.  It adds the ability
    to compare two instances of this class or of derived classes.
    Comparisons are done in "name major" order.  That is, names are
    compared first then codes.  Closures are not compared.
    """

    def __lt__(self, other):
        return self.name < other.name or self.name == other.name and self.code < other.code

    def __le__(self, other):
        return self.name <= other.name or self.name == other.name and self.code <= other.code

    def __eq__(self, other):
        return self.name == other.name and self.code == other.code

    def __ne__(self, other):
        return self.name != other.name and self.code != other.code

    def __gt__(self, other):
        return self.name > other.name or self.name == other.name and self.code > other.code

    def __ge__(self, other):
        return self.name >= other.name or self.name == other.name and self.code >= other.code


class CodeMajorCoding(Coding):
    """
    *CodeMajorCoding* is a subclass of *Coding* and as such inherits
    all of the functionality of the Coding class.  It adds the ability
    to compare two instances of this class or of derived classes.
    Comparisons are done in "code major" order.  That is, codes are
    compared first then names.  Closures are not compared.
    """

    def __lt__(self, other):
        return self.code < other.code or self.code == other.code and self.name < other.name

    def __le__(self, other):
        return self.code <= other.code or self.code == other.code and self.name <= other.name

    def __eq__(self, other):
        return self.code == other.code and self.name == other.name

    def __ne__(self, other):
        return self.code != other.code and self.name != other.name

    def __gt__(self, other):
        return self.code > other.code or self.code == other.code and self.name > other.name

    def __ge__(self, other):
        return self.code >= other.code or self.code == other.code and self.name >= other.name
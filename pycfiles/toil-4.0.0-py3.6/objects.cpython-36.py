# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/objects.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 7617 bytes
from __future__ import absolute_import
from builtins import object
from toil.lib.memoize import sync_memoize

class abstractclassmethod(classmethod):
    __doc__ = "\n    This class defines a decorator that allows the decorated class to be both an abstract method\n    and a class method.\n\n    Shamelessly stolen from\n\n    http://stackoverflow.com/questions/11217878/python-2-7-combine-abc-abstractmethod-and-classmethod\n\n    >>> from abc import ABCMeta\n\n    >>> class DemoABC:\n    ...     __metaclass__ = ABCMeta\n    ...\n    ...     @abstractclassmethod\n    ...     def from_int(cls, n):\n    ...         return cls()\n\n    >>> class DemoConcrete(DemoABC):\n    ...     @classmethod\n    ...     def from_int(cls, n):\n    ...         return cls(2*n)\n    ...\n    ...     def __init__(self, n):\n    ...         print ('Initializing with %s' % n)\n\n    >>> d = DemoConcrete(5)  # Succeeds by calling a concrete __init__()\n    Initializing with 5\n\n    >>> d = DemoConcrete.from_int(5)  # Succeeds by calling a concrete from_int()\n    Initializing with 10\n    "
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


class abstractstaticmethod(staticmethod):
    __doc__ = '\n    This class defines a decorator that allows the decorated class to be both an abstract method\n    and a static method.\n\n    Based on code found at\n\n    http://stackoverflow.com/questions/11217878/python-2-7-combine-abc-abstractmethod-and-classmethod\n\n    >>> from abc import ABCMeta\n\n    >>> class DemoABC:\n    ...     __metaclass__ = ABCMeta\n    ...\n    ...     @abstractstaticmethod\n    ...     def f(n):\n    ...         raise NotImplementedError()\n\n    >>> class DemoConcrete(DemoABC):\n    ...     @staticmethod\n    ...     def f(n):\n    ...         return 2*n\n\n    >>> d = DemoABC.f(5)  # Fails because f() is not implemented\n    Traceback (most recent call last):\n    ...\n    NotImplementedError\n\n    >>> DemoConcrete.f(5)  # Succeeds by calling a concrete f()\n    10\n    '
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractstaticmethod, self).__init__(callable)


class InnerClass(object):
    __doc__ = "\n    Note that this is EXPERIMENTAL code.\n\n    A nested class (the inner class) decorated with this will have an additional attribute called\n    'outer' referencing the instance of the nesting class (the outer class) that was used to\n    create the inner class. The outer instance does not need to be passed to the inner class's\n    constructor, it will be set magically. Shamelessly stolen from\n\n    http://stackoverflow.com/questions/2278426/inner-classes-how-can-i-get-the-outer-class-object-at-construction-time#answer-2278595.\n\n    with names made more descriptive (I hope) and added caching of the BoundInner classes.\n\n    Caveat: Within the inner class, self.__class__ will not be the inner class but a dynamically\n    created subclass thereof. It's name will be the same as that of the inner class,\n    but its __module__ will be different. There will be one such dynamic subclass per inner class\n    and instance of outer class, if that outer class instance created any instances of inner the\n    class.\n\n    >>> class Outer(object):\n    ...     def new_inner(self):\n    ...         # self is an instance of the outer class\n    ...         inner = self.Inner()\n    ...         # the inner instance's 'outer' attribute is set to the outer instance\n    ...         assert inner.outer is self\n    ...         return inner\n    ...     @InnerClass\n    ...     class Inner(object):\n    ...         def get_outer(self):\n    ...             return self.outer\n    ...         @classmethod\n    ...         def new_inner(cls):\n    ...             return cls()\n    >>> o = Outer()\n    >>> i = o.new_inner()\n    >>> i # doctest: +ELLIPSIS\n    <toil.lib.objects.Inner...> bound to <toil.lib.objects.Outer object at ...>\n\n    >>> i.get_outer() # doctest: +ELLIPSIS\n    <toil.lib.objects.Outer object at ...>\n\n    Now with inheritance for both inner and outer:\n\n    >>> class DerivedOuter(Outer):\n    ...     def new_inner(self):\n    ...         return self.DerivedInner()\n    ...     @InnerClass\n    ...     class DerivedInner(Outer.Inner):\n    ...         def get_outer(self):\n    ...             assert super( DerivedOuter.DerivedInner, self ).get_outer() == self.outer\n    ...             return self.outer\n    >>> derived_outer = DerivedOuter()\n    >>> derived_inner = derived_outer.new_inner()\n    >>> derived_inner # doctest: +ELLIPSIS\n    <toil.lib.objects...> bound to <toil.lib.objects.DerivedOuter object at ...>\n\n    >>> derived_inner.get_outer() # doctest: +ELLIPSIS\n    <toil.lib.objects.DerivedOuter object at ...>\n\n    Test a static references:\n    >>> Outer.Inner # doctest: +ELLIPSIS\n    <class 'toil.lib.objects...Inner'>\n    >>> DerivedOuter.Inner # doctest: +ELLIPSIS\n    <class 'toil.lib.objects...Inner'>\n    >>> DerivedOuter.DerivedInner #doctest: +ELLIPSIS\n    <class 'toil.lib.objects...DerivedInner'>\n\n    Can't decorate top-level classes. Unfortunately, this is detected when the instance is\n    created, not when the class is defined.\n    >>> @InnerClass\n    ... class Foo(object):\n    ...    pass\n    >>> Foo()\n    Traceback (most recent call last):\n    ...\n    RuntimeError: Inner classes must be nested in another class.\n\n    All inner instances should refer to a single outer instance:\n    >>> o = Outer()\n    >>> o.new_inner().outer == o == o.new_inner().outer\n    True\n\n    All inner instances should be of the same class ...\n    >>> o.new_inner().__class__ == o.new_inner().__class__\n    True\n\n    ... but that class isn't the inner class ...\n    >>> o.new_inner().__class__ != Outer.Inner\n    True\n\n    ... but a subclass of the inner class.\n    >>> isinstance( o.new_inner(), Outer.Inner )\n    True\n\n    Static and class methods, e.g. should work, too\n\n    >>> o.Inner.new_inner().outer == o\n    True\n    "

    def __init__(self, inner_class):
        super(InnerClass, self).__init__()
        self.inner_class = inner_class

    def __get__(self, instance, owner):
        if instance is None:
            return self.inner_class
        else:
            return self._bind(instance)

    @sync_memoize
    def _bind(self, _outer):

        class BoundInner(self.inner_class):
            outer = _outer

            def __repr__(self):
                return '%s bound to %s' % (super(BoundInner, self).__repr__(), repr(_outer))

        BoundInner.__name__ = self.inner_class.__name__
        BoundInner.__module__ = self.inner_class.__module__
        return BoundInner

    def __call__(*args, **kwargs):
        raise RuntimeError('Inner classes must be nested in another class.')
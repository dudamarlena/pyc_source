# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sflib/delegate.py
# Compiled at: 2009-01-08 03:15:58
"""
delegate.py

A modern, pythonic implementation of the delegate pattern.
This module allows to customize behaviour of class instances without resorting to inheritance.
Instead of deriving a new class, it's possible to add delegation support to an existing class,
and specify a delegate object instance for any desired instance of the said class.
When an instance variable or an instance method will be accessed for these objects, the
corresponding instance variables or instance methods will be retrieved from the delegate objects
instead. If the delegate doesn't define a requested variable or method, this will be searched in
the target instance, as usual.
The description makes it look much more complex than what it is actually. An example can
demonstrate more effectively its use.

Example usage:

  >>> class SimpleClass(object):
  ...     def __init__(self, name):
  ...         self.name = name
  ...
  ...     def sum(self):
  ...         return self.a + self.b
  ...
  ...     def __repr__(self):
  ...         return "SimpleClass(%s)" % self.name
  ...
  ...     def overridden(self):
  ...         return "SimpleClass(%s) method" % self.name

  >>> class SimpleDelegate(object):
  ...     def __init__(self, a, b):
  ...         self.a = a
  ...         self.b = b
  ... 
  ...     def div(self):
  ...         return self.a / self.b
  ...
  ...     def whoami(self):
  ...         return repr(self)
  ...
  ...     def overridden(self):
  ...         return "SimpleDelegate method for %s" % self.delegated
  ...
  ...     def __repr__(self):
  ...         return "SimpleDelegate for %s" % self.delegated

  >>> myobj = SimpleClass('foo')

  >>> add_delegate_support(SimpleClass)

  >>> mydelegate = SimpleDelegate(12, 3)

  >>> add_delegate(myobj, mydelegate)

  >>> print myobj.name
  foo

  >>> print repr(myobj)
  SimpleClass(foo)

  >>> print myobj.div()
  4

  >>> print myobj.sum()
  15

  >>> print myobj.whoami()
  SimpleDelegate for SimpleClass(foo)

  >>> print myobj.overridden()
  SimpleDelegate method for SimpleClass(foo)

  If you need to access a variable or a method in the original instance,
  pass through the `no_delegate` instance object:

  >>> print myobj.no_delegate.overridden()
  SimpleClass(foo) method

  Everything works also if a class with delegation support is further
  extended (by inheritance):

  >>> class A(object):
  ...     def callme(self):
  ...         return "you called A"

  >>> class B(A):
  ...     def callme(self):
  ...         return "you called B"

  >>> class C(B):
  ...     def callme(self):
  ...         return "you called C"

  >>> class BDelegate(object):
  ...     def callme(self):
  ...         return "you called the delegate"

  >>> cobj = C()

  >>> add_delegate_support(B)

  >>> bdelegate = BDelegate()

  >>> add_delegate(cobj, bdelegate)

  >>> cobj.callme()
  'you called the delegate'

  >>> cobj.no_delegate.callme()
  'you called C'

@author: Marco Pantaleoni
@contact: Marco Pantaleoni <panta@elasticworld.org>
@contact: Marco Pantaleoni <marco.pantaleoni@gmail.com>
@copyright: Copyright (C) 2008 Marco Pantaleoni. All rights reserved.
"""

def _delegator_getattribute(self, name, parent_cls=object):
    """
    This is the piggybacked __getattribute__() method of the delegator class.
    """
    if name == 'delegate':
        return parent_cls.__getattribute__(self, name)
    try:
        delegate = parent_cls.__getattribute__(self, 'delegate')
        return delegate.__getattribute__(name)
    except AttributeError:
        return parent_cls.__getattribute__(self, name)


def add_delegate_support(target_cls, parent_cls=object):
    """
    Add delegation support to `target_cls`.
    """

    class _OriginalProxy(object):
        __module__ = __name__

        def __init__(self, obj):
            self._op_obj = obj

        def __getattribute__(self, name):
            if name == '_op_obj':
                return object.__getattribute__(self, name)
            return parent_cls.__getattribute__(self._op_obj, name)

    target_cls.__getattribute__ = lambda self, name, p_cls=parent_cls: _delegator_getattribute(self, name, p_cls)
    target_cls._OriginalProxy = _OriginalProxy


def add_delegate(obj, delegate):
    """
    Add the `delegate` instance as a delegate to object instance `obj`.
    `obj` must be an instance of a new-style class to which delegation support
    has been added.
    The delegate instance is added an instance variable `delegated` pointing to `obj`.
    """
    obj.delegate = delegate
    delegate.delegated = obj
    obj.no_delegate = obj._OriginalProxy(obj)


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
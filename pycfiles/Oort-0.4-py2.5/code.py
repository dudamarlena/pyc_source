# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/util/code.py
# Compiled at: 2007-10-01 11:20:52


class autosuper(type):
    """
    Use this as a metaclass for types to set the magic attribute '__super' on
    them. When this is accessed through self the result is an object
    constructed as if super(ThisType, self) had been called. (Makes it a little
    bit more like in Python 3, where super() will work like this attribute.)
    """

    def __init__(cls, name, bases, members):
        super(autosuper, cls).__init__(name, bases, members)
        setattr(cls, '_%s__super' % name, super(cls))


def init_slots(obj, *args, **kwargs):
    data = dict(zip(obj.__slots__, args))
    data.update(kwargs)
    for a in obj.__slots__:
        setattr(obj, a, data.get(a, None))

    return


class SlotStruct(object):
    """
    Base class for making "struct" types with members defined by their
    __slots__ value. Example:

        >>> class Item(SlotStruct):
        ...     __slots__ = 'first', 'last'

        >>> item1 = Item(first='a', last='b')
        >>> item1.first, item1.last
        ('a', 'b')

        >>> item1.middle = '-'
        Traceback (most recent call last):
        ...
        AttributeError: 'Item' object has no attribute 'middle'

        >>> item2 = Item('a', 'b')
        >>> assert (item1.first, item1.last) == (item2.first, item2.last)

        >>> assert item1.make_dict() == {'first': 'a', 'last': 'b'}

    """
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        init_slots(self, *args, **kwargs)

    def __str__(self):
        return '%s instance with %s' % (type(self).__name__, str(self.make_dict()))

    def make_dict(self):
        return dict([ (a, getattr(self, a)) for a in self.__slots__ ])


def property_with_setter(fset):
    attr = '_%s' % fset.func_name
    return property(lambda self: getattr(self, attr), fset, doc=fset.__doc__)


def call(caller, *args):

    def decorator(decorated):
        callArgs = [ (arg, decorated)[(arg is call)] for arg in args ]
        caller(*callArgs)
        return call

    return decorator


class BooleanDecorator(object):
    """
    A documentation helper. Usage:

        >>> contract = BooleanDecorator('interface')
        >>> class T:
        ...     @contract.interface
        ...     def action(self): raise NotImplementedError
        ...
        >>> assert T.action.interface == True
    """
    __slots__ = 'attributes'

    def __init__(self, *args):
        self.attributes = args

    def __getattr__(self, name):
        if name not in self.attributes:
            raise Exception('Unknown attribute: %s' % name)

        def decorator(func):
            setattr(func, name, True)
            return func

        return decorator


contract = BooleanDecorator('template_method', 'default_method', 'helper', 'state_change')

def attrs(**kwargs):
    """
    Generic decorator for setting attributes. Usage:

        >>> @attrs(value="A value", thing=None, other=True)
        ... def f(): pass
        ...
        >>> assert f.value == "A value"
        >>> assert f.thing is None
        >>> assert f.other is True
    """

    def decorator(func):
        for (key, value) in kwargs.items():
            setattr(func, key, value)

        return func

    return decorator
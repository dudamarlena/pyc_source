# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/declarative.py
# Compiled at: 2019-01-21 15:54:41
# Size of source mod 2**32: 8289 bytes
"""Marrow Schema base class definitions.

These are the most frequently used base classes provided by Marrow Schema.
"""
from warnings import warn
from inspect import isroutine
from collections import OrderedDict as odict, deque
from collections.abc import MutableMapping
from .meta import Element

class Container(Element):
    __doc__ = 'The underlying machinery for handling class instantiation for schema elements whose primary purpose is\n\tcontaining other schema elements, i.e. Document, Record, CompoundWidget, etc.\n\t\n\tAssociation of declarative attribute names (at class construction time) is handled by the Element metaclass.\n\t\n\tContainer subclasses have one additional magical property:\n\t\n\t* ``inst.__data__``\n\t  Primary instance data storage for all DataAttribute subclass instances.  Equivalent to ``_data`` from MongoEngine.\n\t'
    __store__ = dict

    def __init__(self, *args, **kw):
        super().__init__()
        arguments = self._process_arguments(args, kw)
        self.__data__ = self.__store__()
        assert isinstance(self.__data__, MutableMapping), 'Data storage attribute __data__ must be a mutable mapping.'
        for name, value in arguments.items():
            setattr(self, name, value)

    def _process_arguments(self, args, kw):
        """Map positional to keyword arguments, identify invalid assignments, and return the result.
                
                This is likely generic enough to be useful as a standalone utility function, and goes to a fair amount of
                effort to ensure raised exceptions are as Python-like as possible.
                """
        if len(args) > len(self.__attributes__):
            raise TypeError('{0} takes no more than {1} argument{2} ({3} given)'.format(self.__class__.__name__, len(self.__attributes__), '' if len(self.__attributes__) == 1 else 's', len(args)))
        names = [name for name in self.__attributes__.keys() if not name[0] != '_' if name == '__name__'][:len(args)]
        duplicates = set(kw.keys()) & set(names)
        if duplicates:
            raise TypeError('{0} got multiple values for keyword argument{1}: {2}'.format(self.__class__.__name__, '' if len(duplicates) == 1 else 's', ', '.join(duplicates)))

        def field_values(args, kw):
            for i, arg in enumerate(self.__attributes__.keys()):
                if len(args):
                    yield (
                     arg, args.popleft())
                if arg in kw:
                    yield (
                     arg, kw.pop(arg))

        result = odict(field_values(deque(args), dict(kw)))
        unknown = set(kw.keys()) - set(result.keys())
        if unknown:
            raise TypeError('{0} got unexpected keyword argument{1}: {2}'.format(self.__class__.__name__, '' if len(unknown) == 1 else 's', ', '.join(unknown)))
        return result


class DataAttribute(Element):
    __doc__ = "Descriptor protocol support for Element subclasses.\n\t\n\tThe base attribute class which implements the descriptor protocol, pulling the instance value of the attribute from\n\tthe containing object's ``__data__`` dictionary.  If an attempt is made to read an attribute that does not have a\n\tcorresponding value in the data dictionary an ``AttributeError`` will be raised.\n\t"

    def __get__(self, obj, cls=None):
        """Executed when retrieving a DataAttribute instance attribute."""
        if obj is None:
            return self
        try:
            return obj.__data__[self.__name__]
        except KeyError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(obj.__class__.__name__, self.__name__))

    def __set__(self, obj, value):
        """Executed when assigning a value to a DataAttribute instance attribute."""
        obj.__data__[self.__name__] = value

    def __delete__(self, obj):
        """Executed via the ``del`` statement with a DataAttribute instance attribute as the argument."""
        del obj.__data__[self.__name__]


class Attribute(Container, DataAttribute):
    __doc__ = 'Re-naming, default value, and container support for data attributes.\n\t\n\tAll "data" is stored in the container\'s ``__data__`` dictionary.  The key defaults to the Attribute\'s instance name\n\tand can be overridden, unlike DataAttribute, by passing a name as the first positional parameter, or as the\n\t``name`` keyword argument.\n\t\n\tMay contain nested Element instances to define properties for your Attribute subclass declaratively.\n\t\n\tIf ``assign`` is True and the default value is ever utilized, immediately pretend the default value was assigned to\n\tthis attribute.  (Override this in subclasses.)\n\t'
    __name__ = DataAttribute()
    default = DataAttribute()
    assign = False

    def __init__(self, *args, **kw):
        if 'name' in kw:
            kw['__name__'] = kw.pop('name')
        (super().__init__)(*args, **kw)

    def __get__(self, obj, cls=None):
        """Executed when retrieving an Attribute instance attribute."""
        if obj is None:
            return self
        try:
            return super().__get__(obj, cls)
        except AttributeError:
            pass

        try:
            default = self.default
        except AttributeError:
            pass
        else:
            value = default() if isroutine(default) else default
            if self.assign:
                self.__set__(obj, value)
            return value
            raise AttributeError("'{0}' object has no attribute '{1}'".format(obj.__class__.__name__, self.__name__))


class CallbackAttribute(Attribute):
    __doc__ = 'An attribute that automatically executes the value upon retrieval, if a callable routine.\n\t\n\tFrequently used by validation, transformation, and object mapper systems.\n\t'

    def __get__(self, obj, cls=None):
        """Executed when retrieving an Attribute instance attribute."""
        if obj is None:
            return self
        value = super().__get__(obj, cls)
        if isroutine(value):
            return value()
        return value


class BaseAttribute(Container):
    __doc__ = 'BaseAttribute is now called Container.'

    def __init__(self, *args, **kw):
        warn('Use of BaseAttribute is deprecated, use Container instead.', DeprecationWarning)
        (super().__init__)(*args, **kw)


class BaseDataAttribute(Container):
    __doc__ = 'BaseDataAttribute is now called DataAttribute.'

    def __init__(self, *args, **kw):
        warn('Use of BaseDataAttribute is deprecated, use DataAttribute instead.', DeprecationWarning)
        (super().__init__)(*args, **kw)
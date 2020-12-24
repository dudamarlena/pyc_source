# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/immutable.py
# Compiled at: 2019-06-17 15:11:31
"""Helpers to make classes partially or completely immutable."""
from __future__ import unicode_literals
from django.utils import six

class __ImmutableAttrsMetaMetaClass(type):
    """Metaclass to prevent attribute modification.

    This is built to be internal to this file, and to prevent attributes from
    being set or deleted on other metaclasses.

    This metaclass can be applied to itself to become a metaclass used for
    attribute guarding on normal classes.
    """

    def __delattr__(cls, name):
        """Delete an attribute on a class.

        This will always fail, preventing class attributes from being deleted.

        Args:
            name (unicode):
                The name of the attribute to delete.

        Raises:
            AttributeError:
                Always raised, preventing deletion.
        """
        raise AttributeError(b'Class attributes cannot be deleted.')

    def __setattr__(cls, name, value):
        """Set an attribute on a class.

        This will always fail, preventing class attributes from being modified.

        Args:
            name (unicode):
                The name of the attribute to set.

            value (object):
                The value to set.

        Raises:
            AttributeError:
                Always raised, preventing modification.
        """
        raise AttributeError(b'Class attributes cannot be modified.')


__ImmutableAttrsMetaClass = six.add_metaclass(__ImmutableAttrsMetaMetaClass)(__ImmutableAttrsMetaMetaClass)

@six.add_metaclass(__ImmutableAttrsMetaMetaClass)
class __ImmutableMetaClass(__ImmutableAttrsMetaClass):
    """Metaclass for providing immutability support for a class.

    This will prevent the class's attributes from being modified outside of
    the class definition, turn off :py:attr:`__dict__` (preventing direct
    access to the attributes), and rename :py:meth:`__init__` to
    :py:meth:`__immutable_init__` so that :py:class:`_ImmutableMixin` can
    control the mutability during initialization.

    This does make the class a lot more strict, preventing things like
    function spies from working, and preventing classes from being dynamic.
    """

    def __new__(cls, name, bases, d):
        """Construct a new class.

        Args:
            name (unicode):
                The name of the class.

            bases (tuple of type):
                The base classes for this class. This will be extended to
                include :py:class:`_ImmutableMixin` as the first base class.

            d (dict):
                The functions and attributes for the class.

        Returns:
            type:
            The new class.
        """
        d.setdefault(b'mutable_attrs', ())
        d.setdefault(b'immutable_attrs', ())
        d[b'__slots__'] = d[b'mutable_attrs'] + d[b'immutable_attrs'] + _ImmutableMixin.__slots__ + ('_mutable', )
        try:
            d[b'__immutable_init__'] = d[b'__init__']
            del d[b'__init__']
            d[b'__init__'] = lambda *args, **kwargs: None
        except KeyError:
            pass

        return type.__new__(cls, name, (_ImmutableMixin,) + bases, d)


@six.add_metaclass(__ImmutableAttrsMetaClass)
class _ImmutableMixin(object):
    """Mixin for immutable classes.

    This allows subclasses to define a list of mutable and immutable
    attributes. Attempting to modify or delete immutable attributes outside of
    the initialization of the class will always fail.

    This should not be directly set on a class. Instead,
    :py:class:`__ImmutableMetaClass` should be used.
    """
    __slots__ = ('immutable_attrs', 'mutable_attrs')
    mutable_attrs = ()
    immutable_attrs = ()

    def __new__(cls, *args, **kwargs):
        """Create an instance of the class.

        This will create an instance of the class, controlling the mutability
        flag so that immutable fields can only be modified during
        initialization.

        Args:
            *args (tuple):
                Positional arguments for the constructor.

            **kwargs (dict):
                Keyword arguments for the constructor.

        Returns:
            object:
            An instance of the class.
        """
        obj = super(_ImmutableMixin, cls).__new__(cls)
        if hasattr(obj, b'__immutable_init__'):
            obj._mutable = True
            obj.__immutable_init__(*args, **kwargs)
        obj._mutable = False
        return obj

    def __setattr__(self, name, value):
        """Set an attribute on an instance.

        This will only allow mutable attributes to be modified after
        initialization.

        Args:
            name (unicode):
                The name of the attribute to modify.

            value (object):
                The new value.

        Raises:
            AttributeError:
                The attribute cannot be modified, or was not found.
        """
        if not getattr(self, b'_mutable', True) and name not in self.mutable_attrs:
            raise AttributeError(b'Cannot modify immutable attribute "%s".' % name)
        super(_ImmutableMixin, self).__setattr__(name, value)

    def __delattr__(self, name):
        """Delete an attribute on an instance.

        This will only allow mutable attributes to be deleted after
        initialization.

        Args:
            name (unicode):
                The name of the attribute to delete.

        Raises:
            AttributeError:
                The attribute cannot be deleted, or was not found.
        """
        if not getattr(self, b'_mutable', True) and name not in self.mutable_attrs:
            raise AttributeError(b'Cannot delete immutable attribute "%s".')
        super(_ImmutableMixin, self).__delattr__(name)


def immutable(cls):
    """Make a class immutable.

    Args:
        cls (type):
            The class to make immutable.

    Returns:
        type:
        The resulting class.
    """
    return six.add_metaclass(__ImmutableMetaClass)(cls)


del __ImmutableAttrsMetaMetaClass
del __ImmutableAttrsMetaClass
__all__ = ('immutable', )
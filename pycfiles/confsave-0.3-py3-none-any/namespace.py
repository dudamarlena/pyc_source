# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/core/namespace.py
# Compiled at: 2019-08-24 21:16:11
__doc__ = b'Classes for creating configuration groups and namespaces.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from . import compat
from . import option as opt

class Namespace(object):
    """A collection of configuration options."""

    def __init__(self, description=None, **options):
        """Initialize the Namespace with options

        Args:
            description (str, optional): A human readable description of what
                the Namespace contains.
            **options: Each keyword should be an Option object which will be
                added to the Namespace.

        Raises:
            TypeError: If an entry is not an Option object.
        """
        self.__doc__ = description
        self._options = {}
        for name, option in compat.iteritems(options):
            self.register(name, option)

        super(Namespace, self).__init__()

    @property
    def description(self):
        """Get the description of what the namespace contains."""
        return self.__doc__

    def get(self, name, default=None):
        """Fetch an option from the dictionary.

        Args:
            name (str): The name of the option.
            default: The value to return if the name is missing.

        Returns:
            any: The value stored by the option.

        This method resolves the option to its value rather than returning
        the option object itself. Use the 'options()' method or this object's
        iter to get the raw options.
        """
        option = self._options.get(name, None)
        if option is None:
            return default
        else:
            return option.__get__(self)

    def set(self, name, value):
        """Set an option value.

        Args:
            name (str): The name of the option.
            value: The value to set the option to.

        Raises:
            AttributeError: If the name is not registered.
            TypeError: If the value is not a string or appropriate native type.
            ValueError: If the value is a string but cannot be coerced.
        """
        if name not in self._options:
            raise AttributeError((b'Option {0} does not exist.').format(name))
        return self._options[name].__set__(self, value)

    def register(self, name, option):
        """Register a new option with the namespace.

        Args:
            name (str): The name to register the option under.
            option (option.Option): The option object to register.

        Raises:
            TypeError: If the option is not an option.Option object.
            ValueError: If the name is already registered.
        """
        if name in self._options:
            raise ValueError((b'Option {0} already exists.').format(name))
        if not isinstance(option, opt.Option):
            raise TypeError(b'Options must be of type Option.')
        self._options[name] = option

    def options(self):
        """Get an iterable of two-tuples containing name and option.

        The name in this case is the name given at registration time which is
        used to identify an option and look it up on the object. The
        option is the actual Option object.
        """
        return compat.iteritems(self._options)

    def __iter__(self):
        """Proxy iter attempts to the 'options' method."""
        return iter(self.options())

    def __setattr__(self, name, value):
        """Proxy attribute sets to the 'register' method if needed.

        If the value is an option object this call gets proxied to 'register'.
        If the value is anything else this method will follow the standard
        setattr behaviour unless the target is an option in which case the
        method is proxied to 'set'.
        """
        if isinstance(value, opt.Option):
            return self.register(name, value)
        if not hasattr(self, name):
            return object.__setattr__(self, name, value)
        if hasattr(self, b'_options') and name in self._options:
            return self.set(name, value)
        return object.__setattr__(self, name, value)

    def __getattr__(self, name):
        """Lookup missing attributes in the options dictionary."""
        if b'_options' not in self.__dict__ or name not in self._options:
            raise AttributeError((b'Option {0} does not exist.').format(name))
        return self.get(name)


class AutoNamespace(Namespace):
    """Namespace which automatically defined options of a given type."""

    def __init__(self, description=None, type=None, **options):
        """Initialize the Namespace with a type generator.

        Args:
            description (str, optional): A human readable description of what
                the Namespace contains.
            type (Option): The Option class to use when generating dynamic
                options.
            **options: Each keyword should be an Option object which will be
                added to the Namespace.

        Raises:
            ValueError: If type is not given or is not an Option class.
            TypeError: If an entry is not an Option object.
        """
        super(AutoNamespace, self).__init__(description=description, **options)
        self._generator = type

    def set(self, name, value):
        """Set an option value.

        Args:
            name (str): The name of the option.
            value: The value to set the option to.

        Raises:
            TypeError: If the value is not a string or appropriate native type.
            ValueError: If the value is a string but cannot be coerced.

        If the name is not registered a new option will be created using the
        option generator.
        """
        if name not in self._options:
            self.register(name, self._generator())
        return self._options[name].__set__(self, value)

    def __setattr__(self, name, value):
        """Proxy attribute sets to the 'register' method if needed.

        If the value is an option object this call gets proxied to 'register'.
        If the value is anything else this method will follow the standard
        setattr behaviour unless the target is an option in which case the
        method is proxied to 'set'.
        """
        if isinstance(value, opt.Option):
            return self.register(name, value)
        if not hasattr(self, name):
            return object.__setattr__(self, name, value)
        if hasattr(self, b'_options') and hasattr(self, b'_generator'):
            return self.set(name, value)
        return object.__setattr__(self, name, value)

    def __getattr__(self, name):
        """Lookup missing attributes in the options dictionary."""
        if b'_options' not in self.__dict__ or b'_generator' not in self.__dict__:
            raise AttributeError((b'Attribute {0} does not exist.').format(name))
        if name not in self._options:
            self._options[name] = self._generator()
        return self.get(name)
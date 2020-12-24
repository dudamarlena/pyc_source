# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/base.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 1366 bytes


class Py3oTypeMixin(object):
    __doc__ = 'Base mixin for Py3o types.\n\n    This mixin implements the methods that allows a class to be subclassed by\n    a :class:`.Py3oTypeConfig` instance according to its configuration values.\n\n    New types will typically inherit from it as well as a builtin or standard\n    class.\n    '

    @classmethod
    def get_type_for_config(cls, config):
        """Create a subclass with attributes extracted from the configuration.

        The keys and values returned by the base class' implementation of the
        :meth:`~Py3oTypeMixin.get_config_attributes` method will be available
        as class attributes in the new subclass.

        :param Py3oTypeConfig config: The configuration to use.
        :returns: The configured subclass for the original type.
        :rtype: type
        """
        return type(cls.__name__, (cls,), cls.get_config_attributes(config))

    @classmethod
    def get_config_attributes(cls, config):
        """Extract the relevant values from the configuration.

        :param Py3oTypeConfig config: The configuration to use.
        :returns: The attributes to add to the class' namespace.
        :rtype: dict
        """
        return {}

    @property
    def odt_value(self):
        """The raw ODT value for the object."""
        return self
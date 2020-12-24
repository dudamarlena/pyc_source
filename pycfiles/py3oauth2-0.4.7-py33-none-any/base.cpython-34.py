# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/base.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 1366 bytes


class Py3oTypeMixin(object):
    """Py3oTypeMixin"""

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
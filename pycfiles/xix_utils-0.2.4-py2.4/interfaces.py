# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/tools/interfaces.py
# Compiled at: 2006-03-02 13:58:59
from xix.utils.comp.interface import Interface, Attribute
__author__ = 'Drew Smathers'

class IParser(Interface):
    """A text/xml parser.
    """
    __module__ = __name__

    def parse(input):
        """Parse input and return parsed object.
        """
        pass


class IOption(Interface):
    """A schema represenation of a tool argument.
    """
    __module__ = __name__
    short_desc = Attribute('Short description flag for CLI\n            ')
    long_desc = Attribute('Long description flag for CLI\n            ')
    dest = Attribute('Destination variable name fto hold resulting value.\n            ')
    type = Attribute('The type of the option - default is string.\n            ')
    help = Attribute('Help string for information on the tool.\n            ')
    default = Attribute('Default value for option.\n            ')
    value = Attribute('The final value assigned to the option.\n            ')


class IOptionCollection(Interface):
    """Collection of Options.  Corresponds roughly to
    Options of optparse.
    """
    __module__ = __name__

    def append(option):
        """Append option to collection.
        """
        pass

    def add_option(*args, **kwargs):
        """Add new option given specified arguments.
        """
        pass

    def __getattr__(name):
        """Getattribute return actual attribute of IOptionCollection
        object (__xxx__) or named option.  For example:

        options.append(Option('-s', dest='foo', default=1))
        options.foo => 1
        """
        pass

    def __setattr__(name, value):
        """If option with named with dest name is in collection, value
        on IOption instance is set to value, otherwise internal dictionary
        should be updated as normal.
        """
        pass
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/exc.py
# Compiled at: 2019-08-24 21:09:08
__doc__ = b'Configuration related exceptions.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

class MissingRequiredOption(ValueError):
    """Represents a required option which has not been set after parsing."""


class NamespaceNotRegistered(AttributeError):
    """Represents an attempt to set values in a non-existent Namespace."""


class OptionNotRegistered(AttributeError):
    """Represents an attempt to set the value for a non-existent Option."""


class UnrecognizedFileExtension(ValueError):
    """Represents a file extension that cannot be parsed."""
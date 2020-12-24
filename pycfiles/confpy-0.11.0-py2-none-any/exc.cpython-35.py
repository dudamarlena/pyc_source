# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/exc.py
# Compiled at: 2019-08-24 21:09:08
# Size of source mod 2**32: 666 bytes
"""Configuration related exceptions."""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

class MissingRequiredOption(ValueError):
    __doc__ = 'Represents a required option which has not been set after parsing.'


class NamespaceNotRegistered(AttributeError):
    __doc__ = 'Represents an attempt to set values in a non-existent Namespace.'


class OptionNotRegistered(AttributeError):
    __doc__ = 'Represents an attempt to set the value for a non-existent Option.'


class UnrecognizedFileExtension(ValueError):
    __doc__ = 'Represents a file extension that cannot be parsed.'